##########################
## send hbar code       ##
## author: Yudi Xu      ##
## version: v0.0.1      ##
## data: 2019 July 16th ##
## project: mini evec   ##
##########################

from evec import transferHbars

# this info should be taken from the web user input. code needs to be updated by full stack developer
fromAccNum = '0.0.34756'
fromPvtKey = '302e020100300506032b6570042204201727a1006f15c43902b372111e28c72087fbdaad53624814f70bf59a68f7352e'
toAccNum = '0.0.34757'
amount = '1000000'

transferHbars(fromAccNum, fromPvtKey, toAccNum, amount)