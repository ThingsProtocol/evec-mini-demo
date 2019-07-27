from GetMac import getMAC
from HederaCalls import createAccount
import paho.mqtt.client as mqtt

broker_url = "broker.mqttdashboard.com"#mqtt.eclipse.org"
broker_port = 1883
my_MAC_address = "test_mac_addr"#getMAC()
my_acc_details = createAccount(my_MAC_address)

def on_message(client, userdata, message):
	msg = message.payload.decode()
	print("Message Received: ", msg)
	print("msg: ",msg)
	
	if msg == my_MAC_address + " AUTHENTICATED":
		print("I am authenticated!")
		##########################################
		#                                        #
		# WRITE YOUR  ACTION HERE        		 #	
		# can send normal messages now onwards   #
		#                                        #
		##########################################
		#e.g.
		client.publish(topic="Hedera",payload=my_MAC_address+";"+"turn on the LED light",qos=1,retain=False)

client = mqtt.Client()
print client
client.on_message = on_message
print on_message
client.connect(broker_url, broker_port)

client.subscribe(topic="Hedera", qos = 1)

#client sends a message to another client:
_payload = my_MAC_address+";" +my_acc_details['accountNum']
client.publish(topic="Hedera", payload=_payload, qos=1,retain=False)

#always stay on the lookout for messages
client.loop_forever()
