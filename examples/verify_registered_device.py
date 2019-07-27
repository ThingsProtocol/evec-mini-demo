##############################
## verify registered device ##
## author: Yudi Xu          ##
## version: v0.0.1          ##
## data: 2019 July 21st     ##
## project: mini evec       ##
##############################


from evec import doAuthentication

device_accNum = "0.0.36360" # pick it from database
mac_address_of_device = "test_mac_address" # pick it from database

authStatus = doAuthentication(device_accNum,mac_address_of_device)
print("authStatus: ", authStatus)
if authStatus:
    print("Client is authenticated.")


