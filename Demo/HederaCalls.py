"""

pip install requests
pip install -U python-dotenv
"""

import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv


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

def load_url_from_dotenv():
	dotenv_path = join(dirname(__file__), '../.env')
	load_dotenv(dotenv_path)
	url = os.getenv('IP_ADDRESS')+':8080/' #REST API exposed in this url
	return url