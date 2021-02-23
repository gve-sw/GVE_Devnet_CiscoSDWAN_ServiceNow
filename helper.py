  
"""
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from webexteamssdk import WebexTeamsAPI
import requests
import os
import re
import json

def get_json_card(filepath):
    # get adaptive card context
    with open(filepath, 'r') as f:
        json_card = json.loads(f.read())
        f.close()
    return json_card

def replace(template: dict, data: dict):
    # replace the values inside the adaptive card
    str_temp = str(template)
    for key in data:
        pattern = "\${" + key + "}"
        str_temp = re.sub(pattern, str(data[key]), str_temp)
    return eval(str_temp)
    
def send_notification(action, sys_id, full_log):
    # send Webex Adaptive Card Notification
    try:
        api = WebexTeamsAPI(access_token=os.environ['WEBEX_ACCESS_TOKEN'])
    except Exception as e:
        return "ERROR: Retrieving the WEBEX TOKEN, check your enviromental variables" + e

    try:    
        to = os.environ['WEBEX_ALERT_USER']
    except Exception as e:
        return "ERROR: Retrieving the WEBEX ALERT USER, check your enviromental variables" + e
    
    try:
        card_template =  get_json_card("servicenow.json")
    except Exception as e:
        return "ERROR: While retrieving the CARD TEMPLATE, check the servicenow.json" + e
    
    try:
        if action == "Incident Created":
            style = "warning"
        else:
            style = "good"       
        template_data = {"sys_id":sys_id, "full_log":full_log, "style":style, "action": action}
        card =replace(card_template,template_data)
        api.messages.create(
            #roomId=WEBEX_ROOM_ID,
            toPersonEmail = to,
            text = action + " on service now sys_id: " + sys_id + '  '+ 'description: The full log for this alert is:  \n' + full_log,
            attachments = [{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card
            }],
        )
    except Exception as e:
        return "ERROR: While sending the Notification" + e

def create_incident(category,impact,desc,urgency,vmanage_alert_id):
    # create incident in ServiceNow
    headers = {"Content-Type":"application/json", "Accept":"application/json"}
    auth = (os.environ['SERVICENOW_USERNAME'], os.environ['SERVICENOW_PASSWORD'])
    try:
        servicenow_caller = requests.get(os.environ['SERVICENOW_INSTANCE'] + "/api/now/table/sys_user?sysparm_query=user_name%3D" + os.environ['SERVICENOW_USERNAME'], auth=auth, headers=headers).json()['result'][0]['name']
    except Exception:
        return "Cannot Get ServiceNow CallerID! Check Variables"
    ticket = {
        "caller_id": servicenow_caller,
        "impact": impact,
        "urgency": urgency,
        "category": category,
        "short_description": vmanage_alert_id,
        "description": "The full log for this alert is:  \n" + desc
    }
    try:
        create_ticket = requests.post(os.environ['SERVICENOW_INSTANCE'] + "/api/now/table/incident", auth=auth, headers=headers, json=ticket)
    except Exception as e:
        return "Error on Creating ServiceNow Ticket! Check your ServiceNow settings or connectivity!"
    servicenow_raw_json = create_ticket.json()

    if os.environ['WEBEX_NOTIFICATION'] == '1':
        try:
            send_notification("Incident Created", servicenow_raw_json["result"]["sys_id"], desc)
        except Exception as e:
            return "Error on Sending Webex Message!If it is not intended to use turn it from enviromental variables!" + print(e)
    return create_ticket.status_code

def get_incident(vmanage_alert_id): 
    headers = {"Content-Type":"application/json", "Accept":"application/json"}
    auth = (os.environ['SERVICENOW_USERNAME'], os.environ['SERVICENOW_PASSWORD'])
    try:
        incident = requests.get(os.environ['SERVICENOW_INSTANCE'] + "/api/now/table/incident", auth=auth, headers=headers)
    except Exception as e:
        return "Error on Getting ServiceNow Incidents! Check your ServiceNow settings or connectivity"

    servicenow_raw_json = incident.json()["result"]
    for items in servicenow_raw_json:
        if items['short_description'] == str(vmanage_alert_id):
            return items['sys_id']
    return incident.status_code


def close_incident(sys_id, state,desc): # state:6 is for resolved
    headers = {"Content-Type":"application/json", "Accept":"application/json"}
    auth = (os.environ['SERVICENOW_USERNAME'], os.environ['SERVICENOW_PASSWORD'])
    data = {
        "state": state,
    }
    try:
        incident = requests.put(os.environ['SERVICENOW_INSTANCE'] + "/api/now/table/incident/" +sys_id, auth=auth, headers=headers, json=data)
    except Exception:
        return "Error on changing state to resolved on ServiceNow! Check your ServiceNow settings and connectivity!"
    servicenow_raw_json = incident.json()["result"]
    if os.environ['WEBEX_NOTIFICATION'] == '1':
        try:
            send_notification("Incident Resolved", sys_id, desc)
        except Exception as e:
            return "Error on Sending Webex Message!If it is not intended to use turn it from enviromental variables!" + print(e)    
    return incident.status_code
