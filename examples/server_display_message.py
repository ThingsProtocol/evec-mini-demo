##########################
## server mqtt message  ##
## author: Yudi Xu      ##
## version: v0.0.1      ##
## data: 2019 July 16th ##
## project: mini evec   ##
##########################

# separate mqtt app running on the server to listen to the topic to display mqtt topic message. Message is displayed on Web App

import paho.mqtt.client as mqtt

broker_url = "broker.mqttdashboard.com"#mqtt.eclipse.org"
broker_port = 1883

#callback function to print out msg listen from the topic
def on_message(client, userdata, message):
	msg = message.payload.decode()
	
	print (msg)
	# push the message to the web page
    ##########################
    # 
    # some web page code here!
    #
    ###########################
	

client = mqtt.Client()
print client
client.on_message = on_message
print on_message
client.connect(broker_url, broker_port)

client.subscribe(topic="Web", qos = 1)


#always stay on the lookout for messages
client.loop_forever()
