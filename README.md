[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

# EVEC mini-demo project - IoT with Hedera (evec-mini-v0.1)

**Project Description** - 
To test the EVEC's IoT API (mini-release version) on Hedera testnet & mainnet. EVEC is building a distributed IoT toolkit to enpower IoT developers to manage IoT devices (securely) with Distributed Ledger Technology.

This demo project is part of the big **IoT Platform Evolution Program**. By leveraging the new advanced DLT architecture, we will ecolutionize the IoT ecosystem in **Security**, **Interoperability**, **Application development** 

More info will be realesed after summer 2019. Stay Tuned! 


evec-mini-v0.1 is built with Hedera Java SDK and Python. Code has been tested both on VM and raspberry pi (2&3). 


## CONTENTS
1. Environment Set-Up
2. Other Notes

## 1. Environment Set-Up

### 1a.Prerequisites
Before starting ensure you have the following:

**On your Computer** - 

* **Latest** Hedera TestNet Account (created during or after the second  community testing phase)
* [JDK](https://www.oracle.com/technetwork/java/javase/downloads/jdk10-downloads-4416644.html) : 11.x
* [Maven](https://maven.apache.org/) : 3.6.0
* If you are not familiar with JDK and Maven, refer this tutorial to install them [run hashgraph java sdk demo in 5 min (non-developer proof)](https://www.youtube.com/watch?v=7nJ3OW0AP8I)

**On your IoT device** - 

Install `Raspbian` OS
Confirm you have `Python3` and `pip` installed on the raspberry pi (python2 will also work)

### 1b. Installation

* `git clone` this repo on your laptop.
* Also save the (Demo folder)[/Demo] and `.env` on your Raspi device.

#### On your Computer Command Prompt: 
`cd` into the parent folder (i.e. wherever you downloaded this repository)
```
$ mvn install
```

#### On the Pi
```
$ pip install requests
$ pip install -U python-dotenv
```

### 1c. Set-Up

* Update [the env file](.env) with your account details. (Leave FILE_NUM and IP_ADDRESS as it is)
* cd into this folder and run the code by executing the following command
``` $ mvn spring-boot:run```
* from the command line output, get the file number
* In the .env file, write this number next to FILE_NUM (instead of 0)
* Add the IP Address of your laptop to the .env file. (This is so that the rest apis exposed by the laptop can be called by the raspberry pi), make sure this .env file stored on each of your Raspi/IoT device.
	
### 1d. Running the Code
* After following the above steps, once again run the code-
``` $ mvn spring boot:run```.
* Wait for command line output to show "You may call the Rest APIs now!".
* Now you can run `SenseHatDemo.py` (this requires a SenseHAT and Raspi), you will see the Led light turns on and off. 
* If the first demo is successful, you can try our second demo to run `client2.py` followed by `client1.py`. More detailed info can be found in the README.md file in [Demo folder](/Demo).
* A UI-based example and instructions can be found in the [example folder](/examples).


## 2. Notes and Guidelines
* Main functionality lies in [here](/src/main/java/com/freelance/yudi/hashgraph)
* To run the hedera file etc. ensure you have sufficient funds. 
* This functionality is up to date for [SDK 0.4.6 OF HEDERA-JAVA-SDK](https://github.com/hashgraph/hedera-sdk-java)






