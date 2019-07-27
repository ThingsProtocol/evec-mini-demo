package com.freelance.yudi.hashgraph;

import org.springframework.stereotype.Service;

import com.freelance.yudi.utilities.Helper;
import com.hedera.hashgraph.sdk.HederaException;
import com.hedera.hashgraph.sdk.file.FileAppendTransaction;
import com.hedera.hashgraph.sdk.file.FileContentsQuery;
import com.hedera.hashgraph.sdk.file.FileCreateTransaction;
import com.hedera.hashgraph.sdk.file.FileId;
import com.hedera.hashgraph.sdk.account.AccountId;
import com.hedera.hashgraph.sdk.account.AccountCreateTransaction;
import com.hedera.hashgraph.sdk.crypto.ed25519.Ed25519PrivateKey;
import com.hedera.hashgraph.sdk.Client;

import java.time.Duration;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map; //this import is from Sugandh, it was used in makeNewClient() class

@Service
public class FileService {
	
	int FILE_NUM;
	
	Client client;
	
	HashMap<Long,String> fileContents = new HashMap<>();
	
	public FileService() throws Exception {
		
		client = Helper.createHederaClient();
		FILE_NUM = Helper.getHederaFileNumber();
		if (FILE_NUM == 0) { // no hedera file number - create new!
			System.out.println("Creating new Hedera file");
			createFile();
			System.out.println("###########################################");
        	System.out.println("Add the file number in .env file and run code again!");
        	System.out.println("###########################################");
        	System.exit(0);
		} 
	}
	
	//Creates file on the test net.
	public void createFile() throws HederaException {
		
		var operatorKey = Helper.getOperatorKey();        
        var fileContents = "".getBytes();

        var tx = new FileCreateTransaction(client).setExpirationTime(
            Instant.now()
                .plus(Duration.ofSeconds(2592000))
        )
            // Use the same key as the operator to "own" this file
            .addKey(operatorKey.getPublicKey())
            .setContents(fileContents);

        var receipt = tx.executeForReceipt();
        var newFileId = receipt.getFileId();

        System.out.println("file: " + newFileId);
	}
	
	//FILE RELATED APIs...
	
	/**
	 * Reads all contents of the file and appropriately stores them in a mapping
	 * @return mapping of accountID => content stored
	 */
	public void readAllFileContents() throws HederaException {
		var tx = new FileContentsQuery(client).setFileId(new FileId(0,0,FILE_NUM));
		
		try {
			String allContents = tx.execute().getFileContents().toString();
			String fromFirst = allContents.substring(allContents.indexOf("id:"),allContents.length()-2);	
			String[] data = fromFirst.split(";");
			
			for (String str : data) {
				//str = "id:2017DATA:whatever"				
				Long accNum = Long.parseLong(str.substring(3,str.indexOf("DATA:")));
				String content = str.substring(str.indexOf("DATA:")+5);
				fileContents.put(accNum,content);
			}
			System.out.println(fileContents);
		} catch (HederaException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (StringIndexOutOfBoundsException e) {}
	}
	

	//#Sugandh, read data of a particular account. (this one Rahul didn't implement)
	public String readContentsOfAnAccount(String accNum) throws HederaException {
		readAllFileContents();
		long accNumber = AccountId.fromString(accNum).getAccountNum();
		if (fileContents != null && !fileContents.isEmpty()) {
			String value = fileContents.get(accNumber);
			return (value != null ? value : "NO such data");
		}
		return "ERROR in reading the file contents OR No file is empty";
	}	



	/**
	 * Reads Hedera File and checks if data stored against an accountNum is same as data sent
	 * @param accId - hedera account ID whose MAC address has to be verified
	 * @param MAC_Addr - of the device with accId as account ID
	 * @return true if stored value of this accId on file is same as hash of MAC_Addr
	 * @throws Exception 
	 */
	public boolean checkIfStoredOnFile(String accId,String MAC_Addr) throws Exception {
		readAllFileContents();
		String input_hashed_MAC_Addr = Helper.hashMacAddress(MAC_Addr);
		System.out.println("hashed text sent:" + input_hashed_MAC_Addr);
		long accNum = AccountId.fromString(accId).getAccountNum();
		if (fileContents != null && !fileContents.isEmpty()) {
			String value = fileContents.get(accNum);
			System.out.println("hashed text stored:" + value);
			return (value != null && value.equals(input_hashed_MAC_Addr) ? true : false);
		}
		return false;
	}
	
	/**
	 * Appends account specific data to hedera file
	 * @param data - data to add
	 * @param accountId - account number 
	 * @return
	 * @throws HederaException
	 */
	public String appendData_Rahul(String data, String accountId)
			throws HederaException {
				
		FileId fileId = new FileId(0,0,FILE_NUM);			
		
		long accountNum = AccountId.fromString(accountId).getAccountNum();
		
		String updatedData;
		updatedData = "id:"+accountNum+"DATA:"+data+";"; //; is the delimeter.

		var tx = new FileAppendTransaction(client).setFileId(fileId)
					.setContents(updatedData.getBytes());
		try {
			tx.executeForReceipt();
			System.out.println("appended: " + updatedData);
			//fileContents.put(accountNum,data);
	        return "success";
		} catch (HederaException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return e.toString();
		}
	}
	

		/**
	 * Appends account specific data to hedera file, code from Sugandh, 
	    to link the function in FileController addData
	 * @param data - data to add
	 * @param accountId - account number
	 * @param pvtKey - private key of the account.
	 * @param toAccountNum - 
	 * @return
	 * @throws HederaException
	 */
	public String appendData(String data, String accountId, String pvtKey, String toAccountNum)
			throws HederaException {
				
		FileId fileId = new FileId(0,0,FILE_NUM);
		/*Ed25519PrivateKey pvtKeyEDInstance = Ed25519PrivateKey.fromString(pvtKey);
		
		Client currClient = makeNewClient(accountId,pvtKey);
		
		var tx1 = new FileUpdateTransaction(currClient).setFile(fileId)
				.addKey(pvtKeyEDInstance.getPublicKey());
		tx1.executeForReceipt();	
		*/	
		
		long accountNum = AccountId.fromString(accountId).getAccountNum();
		
		String updatedData;
		if(toAccountNum.equals(""))
			updatedData = "id:"+accountNum+"DATA:"+data;
		else
			updatedData = "id:"+toAccountNum+"DATA:"+data;
		
		var tx = new FileAppendTransaction(client).setFileId(fileId)
					.setContents(updatedData.getBytes());
		try {
			tx.executeForReceipt();
			System.out.println("appended: " + data);
			fileContents.put(accountNum,data);
	        return "success";
		} catch (HederaException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return e.toString();
		}
	}






	//ACCOUNT related APIs...
	
	/**
	 * Creates a new account
	 * @param startBalance initial balance
	 * @return array: account Number, public Key, private key
	 * @throws Exception
	 */
	public String[] createNewAccount(long startBalance, String macAddress) throws Exception {
		
		// Generate a Ed25519 private, public key pair
        var newKey = Ed25519PrivateKey.generate();
        var newPublicKey = newKey.getPublicKey();
		
        System.out.println("private key = " + newKey);
        System.out.println("public key = " + newPublicKey);

        //hash macAddress
        String hashed_MAC_Addr = Helper.hashMacAddress(macAddress);
        System.out.println("mac_addr = " + hashed_MAC_Addr);
		
        var tx = new AccountCreateTransaction(client)
            // The only _required_ property here is `key`
            .setKey(newKey.getPublicKey())
            .setInitialBalance(startBalance);
        
        try {
			
			var receipt = tx.executeForReceipt();
	        var newAccountId = receipt.getAccountId();
			
	        System.out.println("New account number = " + newAccountId);
			
	        String[] res = new String[] {newAccountId.toString(),newPublicKey.toString(),newKey.toString()};
	        String res_appendData = appendData_Rahul(hashed_MAC_Addr,newAccountId.toString());
	        //if error on appending hashed address to Hedera File, return error!
	        if (!res_appendData.equals("success"))
	        	return new String[] {res_appendData};
	        return res;
		} catch (HederaException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return new String[] {e.toString()};
		}        
	}


	// #Sugandh, below is new from Sugandh
	/**
	 * Gives balance of an account numbers. Makes the account pay for the query
	 * @param accountNum hedera account number in 0.0.x format
	 * @param privKey private key
	 * @return balance (long)
	 * @throws Exception
	 */	
	public String getBalance(String accountNum, String privKey) throws HederaException {
		
		Client currClient = makeNewClient(accountNum,privKey);
		
		//long balance;
		try {
			long balance = currClient.getAccountBalance(AccountId.fromString(accountNum));
	        System.out.println("Balance for " + accountNum + " = " + balance);
	        return Long.toString(balance);
		} catch (IllegalArgumentException | HederaException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return e.toString();
		}
	}
	
	/**
	 * Allow transferring hbars from one account to another
	 * @param fromAccNum sender Hedera Acc ID in 0.0.x format
	 * @param fromPvtKey sender private key
	 * @param toAccNum receiver account number
	 * @param amount amount to send
	 * @throws Exception
	 */
	public String transferHbars(String fromAccNum, String fromPvtKey, 
			String toAccNum, long amount) throws Exception {
		
		Client currClient = makeNewClient(fromAccNum,fromPvtKey);
		
		try {
			currClient.transferCryptoTo(AccountId.fromString(toAccNum), amount);
	        return("transferred " + amount + " tinybar...");
		} catch (IllegalArgumentException | HederaException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return e.toString();
		}
		/*
		new CryptoTransferTransaction(client)
        // .addSender and .addRecipient can be called as many times as you want as long as the total sum from
        // both sides is equivalent
        .addSender(operatorId, amount)
        .addRecipient(recipientId, amount)
        // As we are sending from the operator we do not need to explicitly sign the transaction
        .executeForReceipt();
        */
	}
	
	//making new originator of a tx - making accounts pay for queries.
	public Client makeNewClient(String accNum, String pvtKey) {
		
		String nodeAddress = Helper.getNodeAddress();
		var client = new Client(Map.of(Helper.getNodeId(), nodeAddress));

        AccountId newOperatorId = AccountId.fromString(accNum);
        Ed25519PrivateKey newOperatorKey = Ed25519PrivateKey.fromString(pvtKey);
        
        // Defaults the operator account ID and key such that all generated transactions will be paid for
        // by this account and be signed by this key
        client.setOperator(newOperatorId, newOperatorKey);

        return client;        
	}	





	
}