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
2. API Documentation
3. Demo Explanation
4. Other Notes

## 1. Environment Set-Up

### 1a.Prerequisites
Before starting ensure you have the following:

**On your Computer** - 

* **Latest** Hedera TestNet Account (created during or after the second  community testing phase)
* [JDK](https://www.oracle.com/technetwork/java/javase/downloads/jdk10-downloads-4416644.html) : 11.x
* [Maven](https://maven.apache.org/) : 3.6.0

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
``` $ mvn spring boot:run```
* Wait for command line output to show "You may call the Rest APIs now!"
* Now you can run `client2.py` followed by `client1.py`

## 2. Hedera API Documentation
2 REST APIs have been built :-

A description of APIs is written in [api_documentation.txt](api_documentation.txt)

To see how to call the APIs refer [HederaCalls.py](/Demo/HederaCalls.py)

## 3. Demo Explanation
Demo code is written in Python and can be found in the [Demo folder](/Demo)
Click [here](/Demo/README.md) for more information on what the demo does

## 4. Notes and Guidelines
* Main functionality lies in [here](/src/main/java/com/freelance/spidertwin1/hashgraph)
* To run the hedera file etc. ensure you have sufficient funds. 
* This functionality is up to date for [SDK 0.4.6 OF HEDERA-JAVA-SDK](https://github.com/hashgraph/hedera-sdk-java)
* To know more about how the demo works refer next section.

---------------------------------------------------------------
# evec mini app prototype (To be created by 31 July)
a demo to show how evec use the distributed power to secure IoT devices - a simple device authenciation scenario to start

A Web UI and the python functions to simplify the life for developers to build IoT App, testing and deploy. 

## Back-end python package
python packages can be found in the folder python_lib (to be created, currently all functions are in example folder)

## example 
python example code can be found in the folder example

## Web UI and flask back-end setup
To be built




