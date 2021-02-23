
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

from flask import Flask, request, jsonify
import requests
import json
import helper
import os

app = Flask(__name__)


@app.route('/', methods=['POST'])
def receive_and_post():
    try:
        print(request.data)  # Check the request coming in
        content = json.loads(request.data)
        if content['active']:
            sys_ip = content['values'][0]['system-ip']
            host_name = content['values'][0]['host-name']
            alarm_msg = content['message']
            alert_level = content['severity_number']
            alert_id = content['uuid']
            try:
                # If there is a site id that is returned
                site_id = content['values'][0]['site-id']
                alert_complete_message = alarm_msg + ' for device ' + sys_ip + ' with site id ' + site_id + ' with hostname ' + host_name
            except:
                alert_complete_message = alarm_msg + ' for device ' + sys_ip + ' with hostname ' + host_name

            try:
                return jsonify(str(
                    helper.create_incident(content['component'], alert_level, alert_complete_message, alert_level,
                                           alert_id)))
            except Exception as e:
                return jsonify('Error on Creating Incident')

        else:
            event_id = content['cleared_events'][0]
            alarm_msg = content['message']
            host_name = content['values'][0]['host-name']
            sys_ip = content['values'][0]['system-ip']
            try:
                sys_id = helper.get_incident(event_id)
                
                try:
                    site_id = content['values'][0]['site-id']
                    alert_complete_message = alarm_msg + ' for device ' + sys_ip + ' with site id ' + site_id + ' with hostname ' + host_name 
                except:
                    alert_complete_message = alarm_msg + ' for device ' + sys_ip + ' with hostname ' + host_name
                try:
                    return jsonify(str(helper.close_incident(sys_id, 6,alert_complete_message)))
                except:
                    return jsonify('Error: While Closing the Alert')
            except Exception as e:
                return jsonify('Error: Cannot Find Alert ID to Close')

    except Exception as e:
        return jsonify('Error while Parsing the alert')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3333)
