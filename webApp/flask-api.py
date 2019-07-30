from flask import request
from flask_api import FlaskAPI
from flask_pymongo import PyMongo
from flask_cors import CORS
from evec import transferHbars

from evec import getMAC 
from evec import createAccount
from evec import device_info_input
import json
import paho.mqtt.client as mqtt
from Naked.toolshed.shell import execute_js, muterun_js

from evec import chkBalance
from evec import transferData
from evec import doAuthentication

app = FlaskAPI(__name__)
CORS(app)
#app.config["MONGO_URI"] = "mongodb://uniutrecht01.nine.ch:27017/test_db"
#mongo = PyMongo(app)

# @app.route("/", methods=['GET'])
# def articles_list():
#   """
#   List or create notes.
#   """

#   articles = list(mongo.db.article.find({'year':{'$gt': 2017}}))
#   # arts = []
#   # for article in articles:
#   #   print(article)
#   #   arts +=article['title']
#   # if request.method == 'POST':
#   #   articles = str(request.data.get('text', ''))
#   #   idx = max(articles.keys()) + 1
#   #   articles[idx] = note
#   #   return note_repr(idx), status.HTTP_201_CREATED

#   # request.method == 'GET'
#   return articles[:5]


# @app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
# def notes_detail(key):
#   """
#   Retrieve, update or delete note instances.
#   """
#   # if request.method == 'PUT':
#   #   note = str(request.data.get('text', ''))
#   #   notes[key] = note
#   #   return note_repr(key)

#   # elif request.method == 'DELETE':
#   #   notes.pop(key, None)
#   #   return '', status.HTTP_204_NO_CONTENT

#   # request.method == 'GET'
#   article = mongo.db.article.find_one_or_404({"_id": key})
#   return article




#######################################################################
######################register device code starts######################
#######################################################################


# Register device, this one is NOT working, because of user input still in terminal...
# @app.route("/register_device/", methods=['GET', 'PUT', 'DELETE'])
# def register_device():
#     # publish message via MQTT to topoc #web, python function in server end will subscribe to this and push it to the webpage. 
#   broker_url = "broker.mqttdashboard.com"#mqtt.eclipse.org"
#   broker_port = 1883

#   #callback function to print out msg listen from the topic
#   def register_message(client, userdata, message):
#     msg = message.payload.decode()
#     print("Device client1 is successfully registered, device info as follows:  ",msg)


#   # call device_info_input function to ask user to enter device_info
#   device_info_input()
#   print("Register Device Process Started.....")


#   ####### code to add device in Azure Cloud via nodejs function #######

#   result = execute_js('device_management.js')

#   if result:
#       print ("JavaScript is successfully executed")
#   else:
#       print ("JavaScript is failed")

#   ############################    code end    ########################



#   # get mac addr and call createAccount function
#   my_MAC_address = "test_mac_address"#getMAC()
#   my_acc_details = createAccount(my_MAC_address)
#   ###################################################################################################################
#   # return message exampele: 
#   # ('Created account: ', 
#   # {u'pubKey': u'302a300506032b65700321004666e4c6513df839088fc376330134c48958ec88a9cb1ce0632ed9c4a8845d0a', 
#   # u'pvtKey': u'302e020100300506032b6570042204205ce27a5ba6f80a1edb75e4579bb895a1aef05ab402e040f877bf2e59f46f6c6c', 
#   # u'accountNum': u'0.0.31243'})
#   ###################################################################################################################


#   # read the json file created above
#   with open('data.json', 'r') as json_file:
#       data = json.load(json_file)
#       #print("data: ", data)
#       data['mac_address'] = my_MAC_address
#       data['account_num'] = my_acc_details['accountNum']
#       #print("data after appended: ", data)
    

#   # write to the json file to update it
#   with open('data.json', 'w') as json_file:
#       json.dump(data, json_file)


#   client = mqtt.Client()
#   client.on_message = register_message
#   client.connect(broker_url, broker_port)
#   client.subscribe(topic="Web", qos = 1)


#   #client sends a message to the topic:
#   _payload = str(data)
#   client.publish(topic="Web", payload=_payload, qos=1,retain=False)

#   #always stay on the lookout for messages, use the on_message callback function to display the message published by itself.
#   #client.loop_forever()
#   client.loop_start()

#   message = {"register device successful, new device info:":_payload}
#   return message

#######################################################################
######################register device code ends########################
#######################################################################

# transfer fund
@app.route("/transfer_fund/", methods=['GET', 'PUT', 'POST', 'DELETE'])
def transfer_fund():
  if request.method in ['OPTIONS', 'POST']:
    #print("yayayay!!!!!!!!", request.data)
    #print("amount", request.data.get("amount"))
    fromAccNum = request.data.get('fromAccNum')#'0.0.34756'
    fromPvtKey = request.data.get('fromPvtKey')#'302e020100300506032b6570042204201727a1006f15c43902b372111e28c72087fbdaad53624814f70bf59a68f7352e'
    toAccNum = request.data.get('toAccNum')#'0.0.34757'
    amount = request.data.get('amount')#'100'
    print ("amount: ", amount)
  
  message = {"output":transferHbars(fromAccNum, fromPvtKey, toAccNum, amount)}
  print (message)

  return message

# check account balance 
@app.route("/balance_check/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def balance_check():
  if request.method in ['OPTIONS', 'POST']:
    device_name = request.data.get('device_name')
    accountNum = request.data.get('accountNum')#'0.0.34756' 
    pvtKey = request.data.get('pvtKey')#'302e020100300506032b6570042204201727a1006f15c43902b372111e28c72087fbdaad53624814f70bf59a68f7352e' # account: 0.0.34756
    currBalance = chkBalance(accountNum,pvtKey)

  message = {"device_name": device_name, "accountNum":accountNum, "currentBalance": currBalance}
  
  return message


# send data to ledger, this api is a bit slow
# @app.route("/message_to_ledger/", methods=['GET', 'PUT', 'DELETE'])
# def message_to_ledger():
#     # this info should be taken from the web user input. code needs to be updated by full stack developer
#   accountNum = '0.0.34756'
#   pvtKey = '302e020100300506032b6570042204201727a1006f15c43902b372111e28c72087fbdaad53624814f70bf59a68f7352e'
#   toAccountNum = '0.0.34757'
#   data = "hellp future 2104!"

#   message = {"output": transferData(data, accountNum, pvtKey, toAccountNum), "data sent": data}

#   return message




# # Server dispaly message, to display the MQTT message send to the topic, works in terminal, but I don't know what to return in this API call.....
# @app.route("/server_display_message/", methods=['GET', 'PUT', 'DELETE'])
# def server_display_message():
#   broker_url = "broker.mqttdashboard.com"#mqtt.eclipse.org"
#   broker_port = 1883

#   #callback function to print out msg listen from the topic
#   def on_message(client, userdata, message):
#     msg = message.payload.decode()
    
#     print (msg)
#     # push the message to the web page
#       ##########################
#       # 
#       # some web page code here!
#       #
#       ###########################
    

#   client = mqtt.Client()
#   print(client)
#   client.on_message = on_message
#   print(on_message)
#   client.connect(broker_url, broker_port)

#   client.subscribe(topic="Web", qos = 1)


#   #always stay on the lookout for messages
#   client.loop_forever()

#   return 

# # verify registered device, this one didn't test successfully
# @app.route("/verify_registered_device/", methods=['GET', 'PUT', 'DELETE'])
# def verify_registered_device():
#   device_accNum = "0.0.36360"# pick it from database
#   mac_address_of_device = "test_mac_address" # pick it from database

#   authStatus = doAuthentication(device_accNum,mac_address_of_device)
#   print("authStatus: ", authStatus)
#   if authStatus:
#       print("Client is authenticated.")
#       message = {"autentication status is:":authStatus}
#   else:
#     message = {"authentication status is:":"failed"}

#   return message

if __name__ == "__main__":
  app.run(debug=True)