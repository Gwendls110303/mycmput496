import cryptomath
from a8_a6 import keyScore
#SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'
SYMBOLS = 'abcdefghijklmnopqrstuvwxyz'
def affine(key, message):
    """
    Decrypts a given cipher text and key using the Affine cipher

    Parameters:
        key: An integer representing the key. See the Chapter 14 to see how
             both keyA and keyB are encoded into a single integer key. 
        message: The string encrypted ciphertext
    """
    keyA = key // len(SYMBOLS)
    keyB = key % len(SYMBOLS)
    plaintext = ''
    modInverseOfKeyA = cryptomath.findModInverse(keyA, len(SYMBOLS))

    if modInverseOfKeyA is None:
        return '.'
    for symbol in message:
        if symbol in SYMBOLS:
            # Decrypt the symbol:
            symbolIndex = SYMBOLS.find(symbol)
            plaintext += SYMBOLS[(symbolIndex - keyB) * modInverseOfKeyA % len(SYMBOLS)]
        else:
            plaintext += symbol # Append the symbol without decrypting.

    return plaintext

keyRange = range(len(SYMBOLS) ** 2)
message = 'ioaboayqimppjojombpgvabynpgcbmnjyqzomblyabynpgcbmnjyjgkodobpjobokmimagzvwiqgzmtgwpkjmpkmipgtoeonpioabopabynpgiyiposiiwajmipjoamoimbaqnjobqzkjqajomajloppobqibonlmaohtypjogzopjboonlmaoivwbpjobgzigmqiambbqohpghtpgoopahonozhohvgbpjoqbioawbqpygzeoonqzcpjoozpqboozabynpqgznbgaoiiioabop'

best_key = ''
best_score = 0

for key in keyRange:

    plaintxt = affine(key, message)
    score = keyScore(plaintxt,message)
    if score > best_score:
        best_key = key
        best_score = score

best_plain = affine(best_key, message)
print('Key:', best_key, 'Plaintext: ', best_plain)