import sys
import logging
import datetime
import time
import os
import requests
import re

from azure.eventhub import EventHubClient, Sender, EventData

logger = logging.getLogger("azure")

# Address can be in either of these formats:
# "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<namespace>.servicebus.windows.net/eventhub"
# "amqps://<namespace>.servicebus.windows.net/<eventhub>"
# SAS policy and key are not required if they are encoded in the URL

ADDRESS = "amqps://<EventHub Namspace>.servicebus.windows.net/<EventHubs Instance>"
USER = "<Access Key Name>"
KEY = "<Primary key value>"

try:
    if not ADDRESS:
        raise ValueError("No EventHubs URL supplied.")

    # Create Event Hubs client
    client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
    sender = client.add_sender(partition="0")
    client.run()
    # VALIDATION PART FOR THE INPUT

    def validateInput(Input_list):
        pattern = re.compile(r'^[A-Za-z]{4}0[A-Z0-9a-z]{6}$')
        numIteration = 0
        while (numIteration < 3):
            address = input("enter your query")
            match_result = re.match(pattern, address)
            if match_result is not None:
                Input_list.append(address)
                numIteration = numIteration + 1
            else:
                print("Try again")
        return Input_list


    try:
        start_time = time.time()
        Input_list = []
        Valid_Input = validateInput(Input_list)
        
        #Grabbing Data from API
        for ifsc in Valid_Input:
            main_api = f'https://ifsc.razorpay.com/{ifsc}'
            json_data = requests.get(main_api).json()
            print("Sending message: {}".format(ifsc))
            
            #creates the message
            message = "BANK:- " + json_data["BANK"] + " , BRANCH:- " + json_data["BRANCH"] + " , CITY:- " + \
                      json_data["CITY"] + " , STATE:-" + json_data["STATE"]
            sender.send(EventData(message))


    except:
        raise
    finally:
        end_time = time.time()
        client.stop()
        run_time = end_time - start_time
        logger.info("Runtime: {} seconds".format(run_time))

except KeyboardInterrupt:
    pass
