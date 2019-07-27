#THIS CODE IN EACH DEVICE

#from sense_hat import SenseHat
import time
import requests
import re
import os
from os.path import join, dirname
from dotenv import load_dotenv
from HederaCalls import createAccount

#sense = SenseHat()

# Accessing variables from .env.
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
url = os.getenv('IP_ADDRESS')+':8080/' #REST API exposed in this url
operator_accNum = os.getenv('OPERATOR_ID')
operator_pvtKey = os.getenv('OPERATOR_KEY')

#sleep function.
msleep = lambda x: time.sleep(x)
print ("Starting read functions....")

#Create Hedera Account





# def createAccount(initialBalance=100000000, ): #
# 	""" Create a hedera account
# 		Parameters
# 		------------
# 		initialBalance : int (default: 100000000)
# 			Account to be initiated with these many tinybars
			
# 		Returns
# 		------------
# 		accDetails : dictionary
# 			Gives account id, public and private key on hedera network.
# 	"""
	
# 	body = {"startBalance": initialBalance } 
# 	print ("body: ", body)
# 	response = requests.post(url+'account', json=body)
# 	print ("url: ", url)
# 	print ("response: ", response)
# 	if response.status_code != 200:
# 		print('POST /tasks/ {}'.format(response.status_code)) 
# 		#raise ApiError?
# 		return None
# 	print('Created account: ', response.json())
# 	accDetails = { 
# 		'pvtKey': response.json()['pvtKey'], 
# 		'accountNum': response.json()['accountNum'], 
# 		'pubKey': response.json()['pubKey']
# 	}
# 	return accDetails

# Read balance function
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
	print ("check balance output: ", response)
	
	regex = "^[-+]?[0-9]+$"
	if re.search(regex,response.content.decode('utf-8')) == None:
	#if response.status_code != 200 or response.content.decode('utf-8')=="-1":
		raise Error("Check that you have enough funds")
	return int(response.content.decode('utf-8'))
	
# Transfer Funds	
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


print ("finish load functions.........")


"""
#demo account
accDetails = {
	'pvtKey': '302e020100300506032b6570042204208de2632d1ffc585fb9d33d43defa82fbc206c3160c999937889f1464cd303ea6', 
	'accountNum': '0.0.4302', 
	'pubKey': '302a300506032b65700321001421b16f4d8a9036fc1137fda61c13e0494833be0ab6267a9b2e643a0f1657c2'
}
"""
print ("just print out test.......")
my_MAC_address = "test_mac_addr"#getMAC()
myAccountDetails = createAccount(my_MAC_address)
print ("myAccountDetails: ", myAccountDetails)

prevBalance = chkBalance(myAccountDetails['accountNum'],myAccountDetails['pvtKey'])
print ("prevBalance: ", prevBalance)
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
		#sense.clear(green) #turn sense green!
		print("Led is Green!")
	else:
		#sense.clear()	#no colour.
		print("Led is off!")
	msleep(2)