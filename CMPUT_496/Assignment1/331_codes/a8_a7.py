#!/usr/bin/env python3

# ---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2023 <<Gwen Delos Santos>>
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
Assignment 7 Problems 2, 3, and 4
"""

import re
from sys import flags
from collections import Counter


def stringIC(text: str):
    """
    Compute the index of coincidence (IC) for text
    """
    freq = Counter(text.upper())
    summation = 0
    for i in freq:
        summation += freq[i]*(freq[i]-1)
    if len(text) >1:
        tot = summation/(len(text)*(len(text)-1))
    else:
        tot =0
    #print('tot',tot)
    return tot


def subseqIC(ciphertext: str, keylen: int):
    """
    Return the average IC of ciphertext for 
    subsequences induced by a given a key length
    """
    freq = Counter(ciphertext.upper())
    subICs = []
    for i in range(keylen):
        #print(getNthSubkeysLetters(nth = keylen, keyLength = keylen, message = ciphertext[i:]))
        subICs.append(stringIC(getNthSubkeysLetters(nth = 1, keyLength = keylen, message = ciphertext[i:])))
    return(sum(subICs)/len(subICs))


def keyLengthIC(ciphertext: str, n: int):
    """
    Return the top n keylengths ordered by likelihood of correctness
    Assumes keylength <= 20
    """
    keyIC = []

    for i in range(1,10): # range of key lengths
        keyIC.append((subseqIC(ciphertext, i), i))
    keyIC = sorted(keyIC, reverse= True)
    return [IC[1] for IC in keyIC[:n]]


def getNthSubkeysLetters(nth: int, keyLength: int, message: str):
    # Returns every nth letter for each keyLength set of letters in text.
    # E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'
    #      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'BBB'
    #      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'CCC'
    #      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'AF'

    # Use a regular expression to remove non-letters from the message:
    message = re.compile('[^A-Z]').sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def test():
    "Run tests"
    assert stringIC("ABA") == 1 / 3
    print('this is for a8', stringIC(''))
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    # #print(stringIC("aaaabbcdddeeeee"))
    # #print(stringIC('aaabbbcccdddeee'))
    # assert( subseqIC('PPQCAXQVEKGYBNKMAZUHKNHONMFRAZCBELGRKUGDDMA', 3) == 0.03882783882783883)
    # assert(subseqIC('PPQCAXQVEKGYBNKMAZUHKNHONMFRAZCBELGRKUGDDMA', 4)==0.0601010101010101)
    # assert( subseqIC('PPQCAXQVEKGYBNKMAZUHKNHONMFRAZCBELGRKUGDDMA', 5)==0.012698412698412698)
    # assert(keyLengthIC('PPQCAXQVEKGYBNKMAZUYBNGBALJONITSZMJYIMVRAGVOHTVRAUCTKSGDDWUOXITLAZUVAVVRAZCVKBQPIWPOU', 5)==[8, 16, 4, 12, 6])
# Invoke test() if called via `python3 a7p234.py`
# but not if `python3 -i a7p234.py` or `from a7p234 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
