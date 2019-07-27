import requests
import re
from sense_hat import SenseHat
import socket
import time

host = '192.168.1.79' #Enter sensehat server ip
port = 5560			  #Enter unused port at which sensehat server is listening

s = SenseHat()

 
url = 'http://localhost:8080/'
operator_accNum = '0.0.1016'						#Your account number
operator_pvtKey = 'Enter your private key here' 	#Your private key
device_name = 'Enter your device name'				#IoT device name

def setupSocket ():		#establish connection with sensehat server
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.connect((host, port))
	return soc

def onBoardDevice (initialbalance):
	#allows you to create a Hedera Account for your current sensehat device with initial balance
	account = createAccount(initialbalance)
	return account
	#gives account id, pub key, priv key which you MUST SAVE for use in function calls

def checkDevice (accountNum, pvtKey):
	#allows you to check current balance for device Hedera account
	chkBalance(accountNum, pvtKey)

def messageToHedera (data, accountNum, pvtKey):
	transferData(data, accountNum, pvtKey)

def sendReceive (soc, message):
	#send msg, get back receiving msg, send close msg
	soc.send(str.encode(message))
	reply = soc.recv(1024)
	print("we have received a reply")
	print("send closing message")
	soc.send(str.encode("EXIT"))
	# soc.close()
	reply = reply.decode('utf-8')
	return reply

def transmit (message) :
	soc = setupSocket()
	response = sendReceive(soc, message)
	return response


# Create Hedera Account
def createAccount(initialbalance=100000000):  #
	""" Create a hedera account
		Parameters
		------------
		initialBalance : int (default: 100000000)
			Account to be initiated with these many tinybars

		Returns
		------------
		accDetails : dictionary
			Gives account id, public and private key on hedera network.
			SAVE THESE DETAILS TO BE USED LATER IN FUNCTION CALLS
	"""

	body = {"startBalance": initialbalance}
	response = requests.post(url + 'account', json=body)
	if response.status_code != 200:
		print('POST /tasks/ {}'.format(response.status_code))
		# raise ApiError?
		return None
	print('Created account: ', response.json())
	accDetails = {
		'pvtKey': response.json()['pvtKey'],
		'accountNum': response.json()['accountNum'],
		'pubKey': response.json()['pubKey'],
		'deviceName': response.json()['deviceName']
	}
	return accDetails


def chkBalance(accountNum, pvtKey):
	""" Check balance of a hedera account
		Parameters
		------------
		accountNum : String
			In the format "<ShardNum>.<Realm Number> . <Account Number>"
			Example: '0.0.4032'
		pvtKey : String
			private key
		Returns
		------------
		balance : int
	"""
	body = {"accountNum": accountNum, "pvtKey": pvtKey }
	response = requests.post(url+'balance', json=body)
	print(device_name, accountNum, currBalance)
	regex = "^[-+]?[0-9]+$"
	if re.search(regex,response.content.decode('utf-8')) == None:
	#if response.status_code != 200 or response.content.decode('utf-8')=="-1":
		raise Exception("Check that you have enough funds")
	return int(response.content.decode('utf-8'))

#Transfer Data
def transferData(data, accountNum, pvtKey, toAccountNum):
	body = {"accountNum": accountNum, "pvtKey": pvtKey, "data": data,
			"toAccountNum": toAccountNum}
	response = requests.post(url+'data', json=body)
	return response.content.decode('utf-8')

# Transfer Crypto
def transferHbars(fromAccNum, fromPvtKey, toAccNum, amount):
	""" Check balance of a hedera account
		Parameters
		------------
		fromAccNum : String
			In the format "<ShardNum>.<Realm Number> . <Account Number>" e.g. '0.0.4032'
			Sender's account id.
		fromPvtKey : String
			sender's private key
		toAccNum 	: String 
			Receiver's account id (e.g.: '0.0.4132')
		amount		: int
			in tinybars.
	"""
	body = {"fromAccountNum": fromAccNum, "fromPvtKey": fromPvtKey, 
			"toAccountNum":toAccNum, "amount":amount }
	response = requests.post(url+'transfer', json=body)
	print (response.content.decode('utf-8'))

"""
#demo account
accDetails = {
	'pvtKey': '302e020100300506032b6570042204208de2632d1ffc585fb9d33d43defa82fbc206c3160c999937889f1464cd303ea6', 
	'accountNum': '0.0.4302', 
	'pubKey': '302a300506032b65700321001421b16f4d8a9036fc1137fda61c13e0494833be0ab6267a9b2e643a0f1657c2'
}
"""

myAccountDetails = createAccount()
prevBalance = chkBalance(myAccountDetails['accountNum'],myAccountDetails['pvtKey'])
green = (0,255,0) #pixel value of green colour
count=0

#every 2 seconds check balance. If balance increases (i.e. transfer occurred), turn green. else off.
while True:
	count+=1
	if count == 3:
		#at 6th second transfer HBars from operator account to account of IoT device.
		transferHbars(operator_accNum,operator_pvtKey,myAccountDetails['accountNum'],100000000)
	currBalance = chkBalance(myAccountDetails['accountNum'],myAccountDetails['pvtKey'])
	if currBalance > prevBalance:
		s.clear(green) #turn sense green!
	else:
		s.clear()	#no colour.
	time.sleep(2)


