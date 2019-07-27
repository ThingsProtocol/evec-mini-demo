import requests
from dotenv import load_dotenv
from HederaCalls import load_url_from_dotenv

#url = 'http://localhost:8080/'


# Read data from Hedera account

def read_message(accNum):
    body ={"accountNum":accNum}
    url = load_url_from_dotenv()
    print ("url: ", url)
    response = requests.post(url+'data_read', json=body)
    return response.json()
    

accNum = "0.0.34757"


print(read_message(accNum))