"""
# This file has code required to get the MAC address of the IoT device calling it
# The IoT device MUST have Raspbian OS, python3 installed
"""

def getEthName():
	# Get name of the Ethernet interface
	try:
		for root,dirs,files in os.walk('/sys/class/net'):
			for dir in dirs:
				if dir[:3]=='enx' or dir[:3]=='eth':
					interface=dir
	except:
		interface="None"
	finally:
		return interface
  
def getMAC():
	# Get the right interface and Return the MAC address
	ethName=getEthName()
	try:
		str = open('/sys/class/net/%s/address' %ethName).read()
	except:
		str = "00:00:00:00:00:00"
	finally:
		return str[0:17]