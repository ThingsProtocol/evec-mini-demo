from HederaCalls import doAuthentication
from GetMac import getMAC
import paho.mqtt.client as mqtt

broker_url = "broker.mqttdashboard.com"#mqtt.eclipse.org"
broker_port = 1883
all_authenticated_clients = []
my_MAC_address = "test"#getMAC()

def on_connect(client, userdata, flags, rc):
	print("Connected With Result Code "+rc)

def on_message(client, userdata, message):
	msg = message.payload.decode()
	print("Message Received: ", msg)
	index = msg.find(";") #get first occurrence of ;
	if index != -1:
		mac_address_of_sender = msg[:index]
		if mac_address_of_sender in all_authenticated_clients:
			print("Client is already authenticated")
			actual_msg = msg[index+1:]
			##########################################
			#                                        #
			# WRITE YOUR  ACTION HERE        		 #			
			#                                        #
			##########################################
			
		
		else :
			print("This client needs to be authenticated.")
			print("Now authenticating ...")
			hedera_account_id_of_sender = msg[index+1:]
			print("hedera_account_id_of_sender: ", hedera_account_id_of_sender)
			authStatus = doAuthentication(hedera_account_id_of_sender,mac_address_of_sender)
			print("authStatus: ", authStatus)
			if authStatus:
				print("Client is authenticated.")
				print("Now client can just send its mac address followed by a semicolon and then its message")
				all_authenticated_clients.append(mac_address_of_sender)
				client.publish(topic="Hedera", payload=mac_address_of_sender+" AUTHENTICATED",qos=1,retain=False)
			else:
				print("Client is not authenticated. MAC Address was wrong. or second half of the message didn;t have the right hedera account number")
	
	elif not(msg.endswith(" AUTHENTICATED")):		
		print("Incorrect message format. Format should be <mac address>;<msg or hedera account id>")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)

client.subscribe("Hedera", qos=1)

#always stay on the lookout for messages
client.loop_forever()