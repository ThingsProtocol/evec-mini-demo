package com.freelance.yudi.hashgraph;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FileController {
	
	/**
	 * APIs:
	 * Create new account 
	 * Do authentication
	 */
	
	@Autowired
	private FileService IoTService;
	
	public FileController() throws Exception {
		IoTService = new FileService();
		System.out.println("###########################################");
    	System.out.println("You may call the REST APIs now!");
    	System.out.println("###########################################");
	}
	
	@RequestMapping(method=RequestMethod.POST,value="/account")
	public HashMap<String,String> createAccount(@RequestBody Map<String, String> json) throws Exception {
		long initialBalance = Long.parseLong(json.get("startBalance"));
		String macAddress = json.get("macAddress");
		String[] res = IoTService.createNewAccount(initialBalance,macAddress);
		HashMap<String,String> mappedRes = new HashMap<>();
		if (res.length!=1) {			
			mappedRes.put("accountNum", res[0]);
			mappedRes.put("pubKey", res[1]);
			mappedRes.put("pvtKey", res[2]);
		} else
			mappedRes.put("error", res[0]);
		return mappedRes;		
	}	
	
	@RequestMapping(method=RequestMethod.POST, value="/auth")
	public boolean doAuthentication(@RequestBody Map<String, String> json) throws Exception {
		String accId = json.get("accountID");
		String MAC_Addr = json.get("MAC_Address_toBeChecked");
		return IoTService.checkIfStoredOnFile(accId,MAC_Addr);
	}

	// #Sugandh, below are all from Sugandh
	// get balance
	@RequestMapping(method=RequestMethod.POST,value="/balance")
	public String getBalance(@RequestBody Map<String, String> json) throws Exception{
		String accountID = json.get("accountNum");
		String pvtKey = json.get("pvtKey");
		return IoTService.getBalance(accountID,pvtKey);
	}

	//transfer
	@RequestMapping(method=RequestMethod.POST,value="/transfer")
	public String transferFunds(@RequestBody Map<String, String> json) throws Exception {
		String fromAccountID = json.get("fromAccountNum");
		String fromPvtKey = json.get("fromPvtKey");
		String toAccNum = json.get("toAccountNum");
		long amount = Long.parseLong(json.get("amount"));
		
		return IoTService.transferHbars(fromAccountID, fromPvtKey, toAccNum, amount);
	}

	

	//add Data
	@RequestMapping(method=RequestMethod.POST,value="/data")
	public String addData(@RequestBody Map<String, String> json) throws Exception {
		String accountID = json.get("accountNum");
		String pvtKey = json.get("pvtKey");
		String data = json.get("data")+";";
		String toAccountID = json.get("toAccountNum");
		
		return IoTService.appendData(data,accountID,pvtKey,toAccountID);
	}

	
	@RequestMapping(method=RequestMethod.POST,value="/data_read")
	public String readData(@RequestBody Map<String, String> json) throws Exception {		
		String accNum = json.get("accountNum");
		return IoTService.readContentsOfAnAccount(accNum);
		
	}


	
	// //read Data
	// @RequestMapping("/data/{id}")
	// public String readData(@PathVariable long id) throws Exception {		
	// 	return IoTService.readContentsOfAnAccount(id);
		
	// }

}
