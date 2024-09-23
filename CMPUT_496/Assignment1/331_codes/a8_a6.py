#!/usr/bin/env python3

#---------------------------------------------------------------
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
#---------------------------------------------------------------

"""
Problem 2
"""

from sys import flags

def ngramsFreqsFromFile(textFile:str, n: int) -> dict:
    """
    Returns a dictionary:
    - Key: a character n-gram (str)
    - Value: frequency of n-gram, num of occur/ tot n-grams (float)
    textFile: 'wells.txt'
    """
    txt = list(open(textFile, 'r').read()) # turns text in file into  a list of characters
    ngrams_freq = {} # for now, key = ngram, value = total count of each ngram
    tot = 0 # total amount of ngrams
    for i in range(len(txt)-(n-1)):
        ngram = ''.join(txt[i:i+n]).upper()
        if ngram in ngrams_freq:
            ngrams_freq[ngram] +=1
        else:
            ngrams_freq[ngram] = 1
        tot +=1

    # Changing dictionary values to be the frequencies rather than counts
    for key in ngrams_freq:
        ngrams_freq[key] = ngrams_freq[key]/tot

    return ngrams_freq

FREQUENCIES = ngramsFreqsFromFile('wells.txt', 3)


def keyScore(plaintxt: str, ciphertext: str, n=3, frequencies=FREQUENCIES) -> float:
    '''
    - Mapping: Dictionary with cipher as key, plain as value
    - Frequencies: A dictionary holding frequencies of ngrams
    This functions gives returns the score of a particular mapping according to it's respective decipherment of a ciphertext
    '''

    
    cipherfreq = {} # dictionary of ngrams as the key and counts as the value

    # make a dictionary of ngrams 
    for i in range(len(plaintxt) - (n-1)): 
        ngram = ''.join(plaintxt[i:i+n]).upper()
        if ngram in cipherfreq:
            cipherfreq[ngram] +=1
        else:
            cipherfreq[ngram] = 1
        
    score = 0    
    # calculates the scores
    for key in cipherfreq: # if key not in frequencies, frequencies = 0 aka do not add anything
        if key in frequencies:
            score +=frequencies[key]*cipherfreq[key]
    return score       



def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking

if __name__ == "__main__" and not flags.interactive:
    #test()

    print(FREQUENCIES)





