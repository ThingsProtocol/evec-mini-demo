# Demo Code

## Explanation

### SenseHAT demo 
In this demo, a new accont is created by the file SenseHatDemo.py, with inital balance of 100,000,000 tiny bar. Everya few second, it code will transfer some Hbars to the IoT device, and check if the balance has increased every 2 second. If balance has increased, blinks the Led, otherwise off. 



### Edge device demo

![EVEC Edge Architecture v0.0.1](/pic/evec edge arch v0.0.1.png?raw=true "evec edge arch v0.0.1")
client1 - c1
client2 - c2

c1 is the sending client. c2 is the receiving client

c1 creates an account on hedera using the rest api and stores its mac address on hedera file.

c1 first sends a message in the format - "c1_mac_address;c1_hedera_account_id"

c2 hears this. checks if message format is valid. Then checks if the mac address in the message has previously been authenticated by it. (If it has - this is where you may add your code). If it hasn't, then c2 calls REST API to talk with Hedera to match the mac address it received against the account number in the message. If the API says the mac address sent matches with the one stored on Hedera File, then c2 broadcasts that c1 is authenticated. 

c1, on hearing this, can now send the actual messages it wanted to send to c2 (this is where you add your code)



## Quick Recap on how to run:

Just as a recap to run the demo from start:

1. Ensure you have prerequisites installed and you filled the .env file correctly
2. from parent directory (on your laptop) run ` $ mvn spring boot:run`
3. Add the newly generated file number in the .env file
4. Run ` $ mvn spring boot:run` and wait for console to output "You may call REST APIs now"
5. Now run `client2.py` followed by `client1.py`

**Note** - when running on IoT device, don't forget to uncomment `line 7 of client1.py` (to get the mac address)
