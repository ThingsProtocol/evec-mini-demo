###############################################################################################
#
# python package evec consists of all the pythnon functions to call Hedera Java SDKs. 
# Current version only support to run the server and IoT devices in the same local network
# Auther: Yudi Xu
# Version: v.0.0.1
# Project code: Sarah
#
###############################################################################################

"""

pip install requests
pip install -U python-dotenv


"""

import requests
import re
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json

# create account 
def createAccount(macAddress, initialBalance="100000000"): #
	""" Create a hedera account and store my MAC address on Hedera File
		Parameters
		------------
		initialBalance : String (default: 0)
			Account to be initiated with these many tinybars
		macAddress : String
			mac address of the iot device (in string)
			
		Returns
		------------
		accDetails : dictionary
			Gives account id, public and private key on hedera network.
	"""
	
	body = {"startBalance": initialBalance, "macAddress": macAddress} 
	url = load_url_from_dotenv()
	response = requests.post(url+'account', json=body)
	
	if response.status_code != 200:
		print('POST /tasks/ {}'.format(response.status_code)) 
		print(response.content)#raise ApiError?
		return None
	print('Created account: ', response.json())
	accDetails = { 
		'pvtKey': response.json()['pvtKey'], 
		'accountNum': response.json()['accountNum'], 
		'pubKey': response.json()['pubKey']
	}
	return accDetails

# do authentication	
def doAuthentication(accountId,macAddressToBeChecked):
	""" Check if the mac address associated to a accountId on Hedera 
	network is indeed the one sent.
		Parameters
		------------
		accountId : String
			Hedera Account ID - {shardNum}.{realmNum}.{accountNum} 
			e.g.: "0.0.13612"
		macAddressToBeChecked : String
			mac address of the iot device to be checked
			
		Returns
		------------
		response : boolean
			true if macAddressToBeChecked == mac address stored on hedera 
			network associated to this account id.
	"""
	body = {"accountID" : accountId,"MAC_Address_toBeChecked":macAddressToBeChecked}
	url = load_url_from_dotenv()
	response = requests.post(url+'auth', json=body)
	if response.status_code != 200:
		print('POST /tasks/ {}'.format(response.status_code)) 
		print(response.content)
		#raise ApiError?
		return None
	return response.json()


# load url from .env file
def load_url_from_dotenv():
	dotenv_path = join(dirname(__file__), '../.env')
	load_dotenv(dotenv_path)
	url = os.getenv('IP_ADDRESS')+':8080/' #REST API exposed in this url
	return url

#Transfer Data
def transferData(data, accountNum, pvtKey, toAccountNum):
	url = load_url_from_dotenv()
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
	url = load_url_from_dotenv()
	body = {"fromAccountNum": fromAccNum, "fromPvtKey": fromPvtKey, 
			"toAccountNum":toAccNum, "amount":amount }
	response = requests.post(url+'transfer', json=body)
	print (response.content.decode('utf-8'))


# check balance
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
	url = load_url_from_dotenv()
	body = {"accountNum": accountNum, "pvtKey": pvtKey }
	response = requests.post(url+'balance', json=body)
	#print(device_name, accountNum, currBalance)
	regex = "^[-+]?[0-9]+$"
	if re.search(regex,response.content.decode('utf-8')) == None:
	#if response.status_code != 200 or response.content.decode('utf-8')=="-1":
		raise Exception("Check that you have enough funds")
	return int(response.content.decode('utf-8'))

# get mac address, this function was only tested in Raspi, Raspian 
def getMAC():
	# Get the right interface and Return the MAC address
	ethName=getEthName()
	try:
		str = open('/sys/class/net/%s/address' %ethName).read()
	except:
		str = "00:00:00:00:00:00"
	finally:
		return str[0:17]


###### register device function starts here ######

# get user input for device tags, return dict format of device attribute
def device_info_input():
    name = raw_input("Enter device Name: ")
    location = raw_input("Enter device location: ")
    device_type = raw_input("Enter device type: ")
    data = { 
        'name': name,
        'location': location,
        'type': device_type
    }

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile) #change this outfile to some web hook etc, to show on the webpage.
    return data




###### register device function end #######

# Read data from Hedera account

def read_message(accNum):
    body ={"accountNum":accNum}
    url = load_url_from_dotenv()
    print ("url: ", url)
    response = requests.post(url+'data_read', json=body)
    return response.json()