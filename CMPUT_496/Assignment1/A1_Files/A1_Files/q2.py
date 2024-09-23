import os
import a8_a6


parentpath = os.path.join(os.getcwd(),'A1_Files','A1_Files')

def get_ciphers(txt_file):
    '''return string of cipher'''
    with open(txt_file, 'r') as f:
        # Read all lines from the file
        cipher = f.readline()

    print(len(cipher))
    return str(cipher)


def xor_ciphers(c1, c2):
    # Convert the two ciphertexts to bytes
    b1 = bytes.fromhex(c1)
    b2 = bytes.fromhex(c2)
    
    # XOR the byte arrays
    return bytes(a ^ b for a, b in zip(b1, b2))

def string_to_hex(s):
    return ''.join(format(ord(c), '02x') for c in s)

def valid(message1, message2):
    # Placeholder validation logic
    # Implement your criteria to check if messages are coherent
    return True  # Replace with actual checks

def brute_decrypt(xor_plaintexts):
    combinations = [...]  # Replace with your list of combinations of length 13
    for message1 in combinations:
        # Convert message1 to hex
        message1_hex = string_to_hex(message1)
        
        # Ensure the lengths match
        if len(message1_hex) != len(xor_plaintexts):
            continue

        # XOR to get message2
        message2_hex = xor_ciphers(xor_plaintexts, message1_hex)
        message2 = message2_hex.decode('utf-8', errors='ignore')

        # Validate and print possible messages
        best_key = ''
        best_score = 0
        for key in potential_keys:
            plaintxt = decryptVigenere(ciphertext, key)
            score = a8_a6.keyScore(plaintxt,ciphertext)
            if score > best_score:
                best_key = key
                best_score = score
        return best_key


  

def main():

    ciphers = {}

    for cipher_file in ['ciphertext1.txt','ciphertext2.txt','ciphertext3.txt']:
        ciphers[cipher_file[:-4]] = get_ciphers(os.path.join(parentpath,cipher_file))

    for cipher in ciphers.values():
        print(cipher)
        print()
 
    hex_c1 = string_to_hex(ciphers['ciphertext1'])
    hex_c2 = string_to_hex(ciphers['ciphertext2'])
    hex_c3 = string_to_hex(ciphers['ciphertext3'])

    for hex in [hex_c1,hex_c2,hex_c3]:
        print(hex)
    # XOR the ciphertexts to eliminate the key
    xor_result = xor_ciphers(hex_c1, hex_c2)

    print("XOR result (hex):", xor_result.hex())

    # Start brute-forcing the decrypted messages
    brute_decrypt(xor_result.hex())

if __name__ == "__main__":
    main()

