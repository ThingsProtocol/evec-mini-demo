package com.freelance.yudi.utilities;

import com.hedera.hashgraph.sdk.account.AccountId;
import com.hedera.hashgraph.sdk.Client;
import com.hedera.hashgraph.sdk.crypto.ed25519.Ed25519PrivateKey;
import io.github.cdimascio.dotenv.Dotenv;

import java.util.Map;
import java.util.Objects;
import java.security.MessageDigest;

public class Helper {
	
	private static String	digits = "0123456789abcdef";
	
    private static Dotenv getEnv() {
        // Load configuration from the environment or a $projectRoot/.env file, if present
        // See .env.sample for an example of what it is looking for
        return Dotenv.load();
    }

    public static AccountId getNodeId() {
        return AccountId.fromString(Objects.requireNonNull(getEnv().get("NODE_ID")));
    }
    
    public static String getNodeAddress() {
    	return Objects.requireNonNull(getEnv().get("NODE_ADDRESS"));
    }

    public static AccountId getOperatorId() {
        return AccountId.fromString(Objects.requireNonNull(getEnv().get("OPERATOR_ID")));
    }

    public static Ed25519PrivateKey getOperatorKey() {
        return Ed25519PrivateKey.fromString(Objects.requireNonNull(getEnv().get("OPERATOR_KEY")));
    }

    public static Client createHederaClient() {
        // To connect to a network with more nodes, add additional entries to the network map
        var nodeAddress = getNodeAddress();
        var client = new Client(Map.of(getNodeId(), nodeAddress));

        // Defaults the operator account ID and key such that all generated transactions will be paid for
        // by this account and be signed by this key
        client.setOperator(getOperatorId(), getOperatorKey());

        return client;
    }
    
    public static int getHederaFileNumber() {
    	return Integer.parseInt(getEnv().get("FILE_NUM"));
    }

    public static byte[] parseHex(String hex) {
        var len = hex.length();
        var data = new byte[len / 2];

        var i = 0;

        //noinspection NullableProblems
        for (var c : (Iterable<Integer>) hex.chars()::iterator) {
            if ((i % 2) == 0) {
                // high nibble
                data[i / 2] = (byte) (Character.digit(c, 16) << 4);
            } else {
                // low nibble
                data[i / 2] &= (byte) Character.digit(c, 16);
            }

            i++;
        }

        return data;
    }
    
    /**
     * Return length many bytes of the passed in byte array as a hex string.     * 
     * @param data the bytes to be converted.
     * @param length the number of bytes in the data block to be converted.
     * @return a hex representation of length bytes of data.
     */
    public static String toHex(byte[] data, int length) {
        StringBuffer	buf = new StringBuffer();
        
        for (int i = 0; i != length; i++) {
            int	v = data[i] & 0xff;
            
            buf.append(digits.charAt(v >> 4));
            buf.append(digits.charAt(v & 0xf));
        }        
        return buf.toString();
    }
    
    //Do a SHA256 hash on input text and return its hex-ed version
    public static String hashMacAddress(String text) throws Exception {
		MessageDigest hash = MessageDigest.getInstance("SHA-256"); 
        hash.update(text.getBytes());
        byte[] hashed = hash.digest();
        String hashed_text = toHex(hashed, hashed.length);
        return hashed_text;
	}
}

