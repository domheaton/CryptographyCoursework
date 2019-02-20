# Author: Dominic Heaton
# Index of Coincidence Calculator
#################################################################################
from langdetect import detect
from guess_language import guess_language
from termcolor import colored
import re
import matplotlib.pylab as plt
import itertools
import os
import collections

def loadFile():
    open_file = open("q1.txt", "r")
    ciphertext = open_file.read().rstrip('\n')
    open_file.close()
    # print(ciphertext)
    return ciphertext

def indexOfCoincidence(ciphertext):
    ciphertext  = "".join([x.upper() for x in ciphertext.split() if  x.isalpha()])
    N = len(ciphertext)
    sumOfFrequency = 0
    alphabet =  map(chr, range( ord('A'), ord('Z')+1))
    letterFrequency = collections.Counter(ciphertext)
    for letter in alphabet:
        sumOfFrequency += letterFrequency[letter] * (letterFrequency[letter] - 1)
    indexOfCoincidence = sumOfFrequency/(N*(N-1))
    return indexOfCoincidence

### MAIN PROGRAM
ciphertext = loadFile()
indexOfCoincidence = indexOfCoincidence(ciphertext)
print(' >Ciphertext: \n' + ciphertext + '\n')
print(' >Index of Coincidence for this Ciphertext is: ' + colored(str(indexOfCoincidence),'red') + '\n')
