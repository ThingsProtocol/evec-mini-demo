import requests
from evec import transferData

#url = 'http://localhost:8080/'


# #Transfer Data
# def transferData(data, accountNum, pvtKey, toAccountNum):
# 	url = load_url_from_dotenv()
# 	body = {"accountNum": accountNum, "pvtKey": pvtKey, "data": data,
# 			"toAccountNum": toAccountNum}
# 	response = requests.post(url+'data', json=body)
# 	return response.content.decode('utf-8')



# this info should be taken from the web user input. code needs to be updated by full stack developer
accountNum = '0.0.34756'
pvtKey = '302e020100300506032b6570042204201727a1006f15c43902b372111e28c72087fbdaad53624814f70bf59a68f7352e'
toAccountNum = '0.0.34757'
data = "hellp future 2104!"

transferData(data, accountNum, pvtKey, toAccountNum)