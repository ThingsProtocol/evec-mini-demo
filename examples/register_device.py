##########################
## register device code ##
## author: Yudi Xu      ##
## version: v0.0.1      ##
## data: 2019 July 16th ##
## project: mini evec   ##
##########################



from evec import getMAC 
from evec import createAccount
from evec import device_info_input
import json
import paho.mqtt.client as mqtt
from Naked.toolshed.shell import execute_js, muterun_js


# publish message via MQTT to topoc #web, python function in server end will subscribe to this and push it to the webpage. 
broker_url = "broker.mqttdashboard.com"#mqtt.eclipse.org"
broker_port = 1883

#callback function to print out msg listen from the topic
def register_message(client, userdata, message):
	msg = message.payload.decode()
	print("Device client1 is successfully registered, device info as follows:  ",msg)


# call device_info_input function to ask user to enter device_info
device_info_input()
print("Register Device Process Started.....")


####### code to add device in Azure Cloud via nodejs function #######

result = execute_js('add_device.js')

if result:
    print ("JavaScript is successfully executed and device is created in Azure IoT Hub!")
else:
    print ("JavaScript is failed")

############################    code end    ########################



# get mac addr and call createAccount function
my_MAC_address = "test_mac_address"#getMAC()
my_acc_details = createAccount(my_MAC_address)
###################################################################################################################
# return message exampele: 
# ('Created account: ', 
# {u'pubKey': u'302a300506032b65700321004666e4c6513df839088fc376330134c48958ec88a9cb1ce0632ed9c4a8845d0a', 
# u'pvtKey': u'302e020100300506032b6570042204205ce27a5ba6f80a1edb75e4579bb895a1aef05ab402e040f877bf2e59f46f6c6c', 
# u'accountNum': u'0.0.31243'})
###################################################################################################################


# read the json file created above
with open('data.json', 'r') as json_file:
    data = json.load(json_file)
    #print("data: ", data)
    data['mac_address'] = my_MAC_address
    data['account_num'] = my_acc_details['accountNum']
    #print("data after appended: ", data)
   

# write to the json file to update it
with open('data.json', 'w') as json_file:
    json.dump(data, json_file)


client = mqtt.Client()
client.on_message = register_message
client.connect(broker_url, broker_port)
client.subscribe(topic="Web", qos = 1)


#client sends a message to the topic:
_payload = str(data)
print ("payload", _payload)
client.publish(topic="Web", payload=_payload, qos=1,retain=False)

#always stay on the lookout for messages, use the on_message callback function to display the message published by itself.
client.loop_forever()
