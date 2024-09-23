#!/usr/bin/env python3

# ---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.1
# Copyright 2023 <<Insert your name here>>
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 331 - Computational Cryptography at the University of
# Alberta, Canada. This solution is confidential and remains confidential
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including
# the URL or other repository locating information, to the following email
# address:
#
#          gkondrak <at> ualberta.ca
#
# ---------------------------------------------------------------

"""
Assignment 8 Problems 1, 2 and 3

# https://www.w3schools.com/python/python_howto_remove_duplicates.asp
"""
from sys import flags
import re, vigenere, string, itertools
from collections import Counter
import a8_a7, a8_a6


# English letter frequencies for calculating IMC (by precentage)
ENG_LETT_FREQ = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 
                 'R': 5.99,  'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 
                 'G': 2.02,  'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 
                 'Q': 0.10,  'Z': 0.07}

def getLetterFrequency(message):
    # t()
    # Returns a dictionary of letter frequencies in the message
    # Divide each letter count by total number of letters in the message to get it's frequency
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 
                   'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 
                   'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 
                   'Y': 0, 'Z': 0}
    
    message = message.upper()
    freq = Counter(message)
    tot = 0
    for char in freq:
        if char in letterCount:
            tot += freq[char]
            letterCount[char] += freq[char]
    
    for char in letterCount:
        letterCount[char] /= tot

    #print("letter freq", letterCount)
    return letterCount

def getSubsequences(ciphertext, keylen):
    # This function takes in a ciphertext as a string and a key length as a int for its parameters
    # This function will return list of lists containing the characters in each subsequence
    subsequences = []
    ciphertext = re.compile('[^A-Z]').sub('', ciphertext)
    for length in range(keylen):
        message = ciphertext[length:]
        letters = []
        i = 0
        while i < len(message):
            letters.append(message[i])
            i += keylen
        subsequences.append(''.join(letters))
    return subsequences

def calculateTopIMC(subsequence):
    # Given a string, this function will calculate and return a list containing all 26 keys and their IMC values
    # Return a list of tuples containing key, IMC pairs from largest IMC to smallest
    subsequence = subsequence.upper()
    IMC_tuples =[]
    for key in string.ascii_uppercase:
        text = decryptVigenere(subsequence, key)
        letter_freq = getLetterFrequency(text)
        tot = 0
        for char in letter_freq.keys():
            tot += letter_freq[char]*(ENG_LETT_FREQ[char])
        IMC_tuples.append((key,tot))
    IMC_tuples.sort(key=lambda x: x[1], reverse = True)
    #print(IMC_tuples)
    return IMC_tuples
    
def topkeys(keychars, subseqs, IMCs, keylength):
    '''IMCs is a dictionary of subsequences and resepctive letter keys. Keychars is a list of letters contatining potentially letters in a key'''
    words = itertools.product(keychars, repeat= keylength)
    keyIMC =[]

    for word in words:
        #input('wait')
        #print('word',word)
        tot_IMC = 0
        for char_i in range(len(word)):
            # finds the IMC value of a letter from each subsequence
            letter_IMC = dict(IMCs[subseqs[char_i]]) # each letter index in the word corresponds to the same index of the subsequence in the list of subsequences
            if word[char_i] in letter_IMC:
                tot_IMC += letter_IMC[word[char_i]]
            else:
                tot_IMC = 0
                break
        if tot_IMC != 0:
            keyIMC.append((''.join(word), tot_IMC))
    keyIMC.sort(key=lambda x: x[1], reverse = True)
    #print(keyIMC)
    return keyIMC[:10]

def decryptVigenere(ciphertext, key):
    # This function takes in a vigenere ciphertext and it's key as the parameters
    # The decrypted message will be returned
    
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    decryption = ''
    return vigenere.vigenere(key,ciphertext,'decrypt')

def vigenereKeySolver(ciphertext: str, keylength: int):
    """
    - Ciphertext: created using the Vigenere Cipher
    - Keylength: length of the key used for the encipherment
    return a list of the ten most likely keys
    """
    # Remove non characters in ciphertext
    ciphertext = re.compile('[^A-Z]').sub('',ciphertext.upper())

    subseqs = getSubsequences(ciphertext, keylength)

    IMCs = {}
    keychars =[]
    if keylength > 7:
        letters_tot = 1
    elif keylength > 5:
        letters_tot = 2
    elif keylength > 4:
        letters_tot = 3
    else:
        letters_tot = 10
    
    for seq in subseqs:
        IMCs[seq] = calculateTopIMC(seq)[:letters_tot] # I only want 10 of the letters for finding the best key 
        tempkeys = [i[0] for i in IMCs[seq]]
        keychars += tempkeys
    #print(IMCs)
    keychars = list(dict.fromkeys(keychars))
    #print(keychars)
    keys = topkeys(keychars,subseqs,IMCs,keylength)
    keys = [word[0] for word in keys]

    print(f'Top keys for len {keylength}:',keys)
    return keys



def hackVigenere(ciphertext: str):
    """
    Use part 1 to get a bunch of random keys
    Use a7 part 4 to deduce the key length keyLengthIC(ciphertext, n) n = how many keys to return
    return a string containing the key to the cipher
    """
    keyLengths = a8_a7.keyLengthIC(ciphertext, 3)
    print("Most likely key lengths", keyLengths)
    temp = list(keyLengths)
    for key in temp:
        if key >10:
            keyLengths.remove(key)
    keys = {} # holds different potential keys

    for length in keyLengths:
        keys[length] = vigenereKeySolver(ciphertext,length)
    potential_keys = []

    for val in keys.values():
        potential_keys += val[:5]

    best_key = ''
    best_score = 0
    for key in potential_keys:
        plaintxt = decryptVigenere(ciphertext, key)
        score = a8_a6.keyScore(plaintxt,ciphertext)
        if score > best_score:
            best_key = key
            best_score = score
    return best_key

def crackPassword(txt):
    """
    hack password_protected.txt and write it to a new file
    """
    #txt = open('password_protected.txt', 'r').read()
    best_key = hackVigenere(txt)
    plain = decryptVigenere(txt,best_key)

    print('Best Key', best_key)
    print('Plain', plain)
    #f = open("plaintext.txt", "w")
   # f.write(plain)
    #f.close()

def test():
    # Letter frequency test
    assert getLetterFrequency('THAT') == {'A': 0.25, 'B': 0.0, 'C': 0.0, 'D': 0.0, 'E': 0.0, 'F': 0.0, 'G': 0.0, 'H': 0.25, 'I': 0.0, 'J': 0.0, 'K': 0.0, 'L': 0.0, 'M': 0.0, 'N': 0.0, 'O': 0.0, 'P': 0.0, 'Q': 0.0, 'R': 0.0, 'S': 0.0, 'T': 0.5, 'U': 0.0, 'V': 0.0, 'W': 0.0, 'X': 0.0, 'Y': 0.0, 'Z': 0.0}

    # # vigenereKeySolver Tests
    # ciphertext = "QPWKALVRXCQZIKGRBPFAEOMFLJMSDZVDHXCXJYEBIMTRQWNMEAIZRVKCVKVLXNEICFZPZCZZHKMLVZVZIZRRQWDKECHOSNYXXLSPMYKVQXJTDCIOMEEXDQVSRXLRLKZHOV"
    # best_keys = vigenereKeySolver(ciphertext, 5)
    # print(hackVigenere(ciphertext))
    # assert best_keys[0] == "EVERY"

    # ciphertext = "Vyc fnweb zghkp wmm ciogq dost kft 13 eobp bdzg uf uwxb jv dxgoncw rtag ymbx vg ucrbrgu rwth gemjzv yrq tgcwxf"
    # best_keys = vigenereKeySolver(ciphertext, 6)
    # assert best_keys[0] == "CRYPTO"
    
    # # hackVigenere Tests
    # ciphertext = "XUOD QK H WRTEMFJI JOEP EBPGOATW JSZSZV OVVQY JWMY JHTNBAVR GU OMLLGG KYODPWU YSWMSH OK ZSSF AVZS BZPW"
    # key = hackVigenere(ciphertext)
    # assert key == "ECGLISH"

    # ciphertext = "A'q nrxx xst nskc epu qr uet zwg'l aqiobfk, uf M gwif ks yarf jsfwspv xh lemv qx ls yfvd. Vmpfwtmvu sivsqg vbmarek e owva csgy xkdi tys. K teg linc mm'k lkd fr llg ner zi ugitcw Jv ghmpfe'x ldigg fxuewji hx xjv rhawg fymkmfv lbk akehho."
    # key = hackVigenere(ciphertext)
    # assert key == "SECRET"
    # print('Done 2')

    # # hackVigenere Tests new
    ciphertext = "ANNMTVOAZPQYYPGYEZQPFEXMUFITOCZISINELOSGMMOAETIKDQGSYXTUTKIYUSKWYXATLCBLGGHGLLWZPEYXKFELIEUNMKJMLRMPSEYIPPOHAVMCRMUQVKTAZKKXVSOOVIEHKKNUMHMFYOAVVMITACZDIZQESKLHARKAVEUTBKXSNMHUNGTNKRKIETEJBJQGGZFQNUNFDEGUU"
    key = hackVigenere(ciphertext)
    assert key == "MAGIC"
    # print('done magic')
    
    # ciphertext = "AQNRXXXSTNSKCEPUQRUETZWGLAQIOBFKUFMGWIFKSYARFJSFWSPVXHLEMVQXLSYFVDVMPFWTMVUSIVSQGVBMAREKEOWVACSGYXKDITYSKTEGLINCMMKLKDFRLLGNERZIUGITCWJVGHMPFEXLDIGGFXUEWJIHXXJVRHAWGFYMKMFVLBKAKEHHO"
    # key = hackVigenere(ciphertext)
    # assert key == "SECRET"
    # print('done secret')

    # ciphertext = "JDMJBQQHSEZNYAGVHDUJKCBQXPIOMUYPLEHQFWGVLRXWXZTKHWRUHKBUXPIGDCKFHBZKFZYWEQAVKCQXPVMMIKPMXRXEWFGCJDIIXQJKJKAGIPIOMRXWXZTKJUTZGEYOKFBLWPSSXLEJWVGQUOSUHLEPFFMFUNVVTBYJKZMUXARNBJBUSLZCJXETDFEIIJTGTPLVFMJDIIPFUJWTAMEHWKTPJOEXTGDSMCEUUOXZEJXWZVXLEQKYMGCAXFPYJYLKACIPEILKOLIKWMWXSLZFJWRVPRUHIMBQYKRUNPYJKTAPYOXDTQ"
    # key = hackVigenere(ciphertext)
    # assert key == "QWERTY"
    # print('done qwerty')
 

if __name__ == '__main__' and not flags.interactive:
    #test()
    crackPassword('leivrazeiiluixpxciwfnetrmctuizyajdxwewzbqegusesmxchvlolrjevucfcdinmtenfdmtrtowffmogtayofspkppzdqedxruleqypzsaopetuuminlfmogpfcpeylmtuyoqvmboiyrflelfcfcuxyhgltgqoertidfzgofnoylzhigbpacatrbbtpfzpeltawwmjfxdtpobermjedsmzeufeyyaxiyjeo')