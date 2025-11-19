import socket
import time
from string import printable

# Connect to the oracle server
def connect_to_oracle(data, max_retries=20, timeout=3):
    retries = 0
    while retries < max_retries:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)  # Set timeout for operations
                s.connect(('10.81.0.35', 4242))
                
                # Read the banner
                response = s.recv(1024)
                # print(response.decode())  # Debug
                
                # Read options
                response = s.recv(1024)
                # print(response.decode())  # Debug
                
                # Choose the encrypt option
                s.sendall(b"1\n")
                
                # Read the encryption prompt
                response = s.recv(1024)
                # print(response.decode())  # Debug
                
                # Send the data to encrypt
                s.sendall(data + b"\n")
                
                # Receive and return the ciphertext
                result = s.recv(2048).strip()
                # print(f"Ciphertext: {result}")  # Debug
                return result
        
        except (socket.timeout, ConnectionError) as e:
            print(f"Connection attempt {retries + 1} failed: {e}")
            retries += 1
            time.sleep(3)  # Wait before retrying

    print("Failed to connect to Oracle server after multiple attempts.")
    return None


# Determine block size
def get_block_size():
    initial_len = len(connect_to_oracle(b"A"))
    for i in range(1, 64):
        new_len = len(connect_to_oracle(b"A" * i))
        print(f"Input Length: {i}, Cipher Length: {new_len}")
        if new_len > initial_len:
            return new_len - initial_len
    return None

# Check if ECB mode
def is_ecb(block_size):
    test_input = b"A" * block_size * 2
    ciphertext = connect_to_oracle(test_input)
    return ciphertext[:block_size] == ciphertext[block_size:block_size * 2]
    
def get_blocks(block):
	new = []
	size = 32
	for i in range(0, len(block), size):
		new.append(block[i:i+size])
	return new

known_data = []


def first_block(start_block_gap):
	input_data = b"A"*(start_block_gap - len(known_data)) 
	Ciphertext = connect_to_oracle(input_data)
	block = get_blocks(Ciphertext.decode('utf-8'))
	return block[0]   # 1
 
# Perform byte-by-byte ECB attack
def ecb_byte_at_a_time():
	for i in range (0,16):
		block_size = 32
		start_block_gap = 15  #31
		block_should_be = first_block(start_block_gap)
#		print(block_should_be)
		
		for c in printable:
			print("Trying String : ", "'"+ "".join(known_data) + c + "'")
#			print("Block Should be : ", block_should_be)
			input_data = b"A"*(start_block_gap - len(known_data)) + "".join(known_data).encode('utf-8') + c.encode('utf-8')
			Ciphertext = connect_to_oracle(input_data)
			block = get_blocks(Ciphertext.decode('utf-8'))
#			print("Getting  blocks : ", block[0] )
			if block[0] == block_should_be:    #1
				print("We got Hit ---")
				print("Character : ", c)
				print(block[0])            #1   
				known_data.append(c)
				print(known_data)
				break
		



# Main logic

secret_suffix = ecb_byte_at_a_time()


#block_size = get_block_size()
#print(f"Detected block size: {block_size}")

#if is_ecb(block_size):
 #   print("Confirmed ECB mode.")

    # print(f"Recovered SECRET_SUFFIX: {secret_suffix.decode()}")
#else:
 #   print("ECB mode not detected.")
