# Author: Dominic Heaton
# Frequency Analysis
##################################################
from collections import Counter
from termcolor import colored

def loadFile():
    open_file = open("q1.txt", "r")
    ciphertext = open_file.read().rstrip('\n')
    open_file.close()
    # print(ciphertext)
    return ciphertext.upper()

def letterFrequency(ct):
    freqAlphabet = {'A' : ct.count('A'), 'B' : ct.count('B'), 'C' : ct.count('C'),
                    'D' : ct.count('D'), 'E' : ct.count('E'), 'F' : ct.count('F'),
                    'G' : ct.count('G'), 'H' : ct.count('H'), 'I' : ct.count('I'),
                    'J' : ct.count('J'), 'K' : ct.count('K'), 'L' : ct.count('L'),
                    'M' : ct.count('M'), 'N' : ct.count('N'), 'O' : ct.count('O'),
                    'P' : ct.count('P'), 'Q' : ct.count('Q'), 'R' : ct.count('R'),
                    'S' : ct.count('S'), 'T' : ct.count('T'), 'U' : ct.count('U'),
                    'V' : ct.count('V'), 'W' : ct.count('W'), 'X' : ct.count('X'),
                    'Y' : ct.count('Y'), 'Z' : ct.count('Z')}
    freqEnglish = {'A': 8.17, 'B': 1.29, 'C': 2.78, 'D': 4.25,'E': 12.70,
                    'F': 2.23, 'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15,
                    'K': 0.77, 'L': 4.03,  'M': 2.41, 'N': 6.75, 'O': 7.51,
                    'P': 1.93, 'Q': 0.10, 'R': 5.99, 'S': 6.33, 'T': 9.06,
                    'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15, 'Y': 1.97,
                    'Z': 0.07} # Frequency values from Wikipedia
    return freqAlphabet, freqEnglish

def maxValKey(dictionary):
    return max(dictionary, key=dictionary.get)

def removeKey(dictionary, key):
    del dictionary[key]

def replaceValue(plaintext, valueToReplace, replacement):
    return plaintext.replace(valueToReplace, replacement)

### Main Program ###
ciphertext = loadFile()
plaintext = ciphertext
freqAlphabet, freqEnglish = letterFrequency(ciphertext)

print(ciphertext)
while(len(freqAlphabet) > 0):
    print('Replacing ' + maxValKey(freqAlphabet) + ' with ' + maxValKey(freqEnglish).lower())
    plaintext = replaceValue(plaintext, maxValKey(freqAlphabet), maxValKey(freqEnglish).lower())
    removeKey(freqAlphabet, maxValKey(freqAlphabet))
    removeKey(freqEnglish, maxValKey(freqEnglish))
    print(plaintext)
    print()
# print(freqAlphabet['a']) # print frequency of 'a'
