##############################
## verify registered device ##
## author: Yudi Xu          ##
## version: v0.0.1          ##
## data: 2019 July 21st     ##
## project: mini evec       ##
##############################


from evec import doAuthentication

device_accNum = # pick it from database
mac_address_of_device = # pick it from database

authStatus = doAuthentication(device_accNum,mac_address_of_device)
print("authStatus: ", authStatus)
if authStatus:
    print("Client is authenticated.")


