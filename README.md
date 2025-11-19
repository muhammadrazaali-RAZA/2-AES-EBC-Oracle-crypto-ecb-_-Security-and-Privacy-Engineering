# 2-AES-EBC-Oracle-crypto-ecb-_-Security-and-Privacy-Engineering
Security and Privacy Engineering course Hacking and Creaking Assignment 2-AES EBC Oracle (crypto-ecb)


### Explanation of How I solved :

Flag was 32 Byte long but gap has 15 len so after 16 byte of flag getting 0000 which was error so I make gap to 31 and match with second block which works perfectly and have a whole script to proide but the description is below

---

### **1. Connecting to the Oracle**
- **Function**: `connect_to_oracle`
- **Purpose**:
  - Establishes a TCP connection with the encryption oracle server.
  - Sends data to be encrypted and retrieves the ciphertext.
---

### **2. Determining the Block Size**
- **Function**: `get_block_size`
- **Purpose**:
  - Determines the block size of the encryption algorithm (e.g., 16 bytes for AES).
- **How It Works**:
  - Encrypts increasingly longer strings of `b"A"` until the ciphertext length increases.
  - The difference in lengths indicates the block size.

---

### **3. Confirming ECB Mode**
- **Function**: `is_ecb`
- **Purpose**:
  - Confirms if the encryption oracle uses **ECB mode**.
- **How It Works**:
  - Encrypts a string with two identical blocks of `b"A"` (`block_size * 2`).
  - Checks if the first two ciphertext blocks are identical, which is characteristic of ECB mode.

---

### **4. Breaking the Ciphertext into Blocks**
- **Function**: `get_blocks`
- **Purpose**:
  - Splits the ciphertext into fixed-sized blocks (default size: 32 characters in hexadecimal, representing 16 bytes).
- **How It Works**:
  - Iterates through the ciphertext in chunks of `size`.

---

### **5. Getting the Target Block**
- **Function**: `first_block`
- **Purpose**:
  - Identifies the block of ciphertext that needs to be matched during the attack.
- **How It Works**:
  - Encrypts a padded string (`b"A" * (start_block_gap - len(known_data))`) and retrieves the first block of the ciphertext.

---

### **6. Performing the Byte-by-Byte Attack**
- **Function**: `ecb_byte_at_a_time`
- **Purpose**:
  - Recovers the secret suffix by exploiting the deterministic nature of ECB mode.
- **How It Works**:
  - For each byte position (16 iterations):
    1. Calculates the target block to match using `first_block`.
    2. Appends each printable character to the `known_data` and encrypts the input.
    3. Compares the first ciphertext block to the target block.
    4. If a match is found:
       - Prints the matching character.
       - Adds the character to `known_data`.
       - Breaks the loop to move to the next byte.
  - This process repeats until all bytes of the secret are recovered.

---

### **7. Results**
- **Recovered Data**:
  - The function incrementally builds the `known_data` list, which holds the recovered plaintext bytes of the secret.

---

### **Flow Summary**
1. **Initialization**:
   - Connect to the server and verify the block size and ECB mode (if enabled).
2. **Attack Logic**:
   - Use a byte-by-byte approach to match ciphertext blocks and reconstruct the hidden data.
3. **Output**:
   - The `known_data` contains the revealed secret.

---

### **Example Output (During the Attack)**:
```plaintext
Trying String: 'A'
We got Hit ---
Character: A
Known data so far: ['A']
Trying String: 'AA'
We got Hit ---
Character: A
Known data so far: ['A', 'A']
...
Recovered SECRET_SUFFIX: FLAG{ECB_attack_successful}
```

---

### **Key Features of the Attack**
1. **Exploitation of ECB Mode**:
   - The attack relies on the deterministic nature of ECB mode: identical plaintext blocks produce identical ciphertext blocks.

2. **Padding to Isolate Target Block**:
   - Padds the input data (`b"A" * (start_block_gap - len(known_data))`) to ensure the unknown secret aligns with a predictable block.

3. **Iterative Discovery**:
   - Recovers one byte at a time by brute-forcing all printable characters.

---
