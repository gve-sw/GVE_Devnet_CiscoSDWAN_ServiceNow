# Cisco SD-WAN ServiceNow Integration

A Flask application to automatically create and resolve incidents in ServiceNow following an alert in SD-WAN, and using a Webex Teams bot to update the admin.

## Contacts
* Efe Evyapan (hevyapan@cisco.com)
* Eda Akturk (eakturk@cisco.com)

## Solution Components
* Cisco SD-WAN 
* Webex Teams
* ServiceNow
* Heroku
* Python

## Solution Overview
![/IMAGES/image1.PNG](/IMAGES/image1.PNG)

## Installation/Configuration

#### Clone the repo :
```$ git clone (link)```

#### *(Optional) Create Virtual Environment :*
Initialize a virtual environment 

```virtualenv venv```

Activate the virtual env

*Windows*   ``` venv\Scripts\activate```

*Linux* ``` source venv/bin/activate```

#### Install the libraries :

```$ pip install -r requirements.txt```

## Setup: 
*Webhook Reciver*
1. Webhooks allow vManage to send HTTP POST request to an external system in real-time once an alarm is received. 
You need a web server that will receive the webhooks from vManage. [Heroku](https://www.heroku.com/), [Pythonanywhere](https://www.pythonanywhere.com/) or [ngrok](https://ngrok.com/) (to run locally) are options that can be used.
*Heroku is used in the demo.* 

*Cisco SD-WAN*


2. Configure Webhooks on V-Manage. You can find the steps to configure Webhooks notifications [here.](https://www.cisco.com/c/en/us/support/docs/routers/sd-wan/214615-vmanage-configure-alarm-email-notificat.html)

*ServiceNow*


3. Add the details of your service now instance to your config variables in heroku or env_var.py if you are running locally. If you do not have a ServiceNow instance you can sign up to the developer program to obtain one from [here.](https://developer.servicenow.com/dev.do)
```
SERVICENOW_USERNAME = " "
SERVICENOW_PASSWORD = " "
SERVICENOW_INSTANCE = " "
```

*Webex Teams Message:*

4. If you would like to receive webex notifications on actions you would need to enable notifications by setting the "WEBEX_NOTIFICATION" in environmental variables as True (or 1 depending on the webserver that is being used). 
```
WEBEX_NOTIFICATION= " "
```

#### *(Optional) Webex Teams Message :*

5. Create a Webex Bot from [here.](https://developer.webex.com/my-apps/new/bot) 

6. Add your Bot Token to your websever variables or env_var.py for running locally. 
```
WEBEX_ACCESS_TOKEN= " "
```
7. Create a Webex Team Space and add the bot to the Space.

8. Add the Webex Space Name to your webserver variables or env_var.py for running locally.  
```
WEBEX_SPACE_NAME= " "
```

#### *(Optional) Edit Webex Teams Card Message :*
9. The appliaction will send adaptive card messages based on the alarms. You can use the card designer [here](https://developer.webex.com/buttons-and-cards-designer) to change the format of the adaptive card. 

10. Once you create your card you can edit the servicenow.json file to be modified according to the new format. 

## Usage

    $ python app.py

When you start the application ServiceNow Tickets and Webex Teams notifications will be created from Webhook notifications from Vmanage. 

<b>Please note:</b> The alarms that have been tested for the project are as follows:
- BFD TLOC DOWN/UP
- BFD BETWEEN SITES DOWN/UP
- BFD NODE DOWN/UP
- BFD SITE DOWN/UP
- Control TLOC DOWN/UP
- System Reboot Issued
- Control Node DOWN/UP

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
