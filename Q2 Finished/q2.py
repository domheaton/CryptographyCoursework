# Author: Dominic Heaton
# Solution Script for Q2
# XOR Cipher Decryption Attempt
# Given first letter of Plaintext is 'I' (capital i), first byte of key can be
#   determined. Brute force of second byte reveals plaintext.
#################################################################################
from langdetect import detect
from guess_language import guess_language
from termcolor import colored
import re
import matplotlib.pylab as plt
import operator
import binascii

def loadFile():
    open_file = open("q2.txt", "r")
    ciphertext = open_file.read().rstrip('\n')
    open_file.close()
    # print(ciphertext)
    return ciphertext

def hexStringToInt(hex):
    return int(hex,16)

def intToAscii(number):
    return chr(number)

def asciiToInt(string):
    return ord(string)

def exportSolution(plaintext, theKey):
    open_file = open("q2-solution.txt", "w")
    open_file.write('Plaintext: ' + plaintext + '\n\nKey: ' + theKey)
    open_file.close()

### MAIN PROGRAM
ciphertext = loadFile()
ciphertext = ciphertext.replace(" ", "")
print('\nStarting Decipher Attempt...\n')
print(' >Ciphertext: \n' + ciphertext + '\n')
key = []

#find key for first letter of text using the hint "I"
cipherByte = ciphertext[:2] #first hex byte
print(' >XOR is reversible. We know the first letter of plaintext is \'I\' and can therefore reverse to find the key')
hintLetter = asciiToInt("I")
key.append(hexStringToInt(cipherByte) ^ hintLetter)
print(' >Key to give \'I\' as plaintext: ' + hex(key[0]))
print(' >This is proved by encrypting \'I\' with key \'0x1a\' to give first ascii letter of ciphertext: ' + intToAscii(hintLetter ^ key[0]))

#attempting to decipher remaining plaintext using the key 0x1a
print('\n >Attempting decryption of the ciphertext using this 1-byte key (0x1a):')
plaintext = 'I'
for i in range(2, len(ciphertext), 2):
    cipherByte = ciphertext[i:i+2]
    plaintext += intToAscii(hexStringToInt(cipherByte) ^ key[0])
print(plaintext)
print('\n >It is clear decryption using the 1-byte key is unsuccessful at revealing plaintext')

#attempting to decipher remaining plaintext using the key 0x1a
print(' >Attempting decryption of the ciphertext using a 2-byte key of form \'1aXX\' where XX is determined by brute force:\n')
plaintext = ''
plaintext2 = ''
decipheredPlaintext = ''

#Decipher ciphertext bytes 1,3,5,7,... with key 0x1a determined before
plaintext = 'I'
for i in range(4, len(ciphertext), 4):
    cipherByte = ciphertext[i:i+2]
    plaintext += intToAscii(hexStringToInt(cipherByte) ^ key[0])

#Decipher ciphertext bytes 2,4,6,8,... with potential keys from 0-256
for i in range(0,256):
    for j in range(2, len(ciphertext), 4):
        cipherByte = ciphertext[j:j+2]
        plaintext2 += intToAscii(hexStringToInt(cipherByte) ^ i)
    #Concatenate together solutions and print potential plaintexts
    for k in range(0,len(plaintext2)):
        decipheredPlaintext += plaintext[k]
        decipheredPlaintext += plaintext2[k]
    #limit printing of plaintext to just english language
    if detect(decipheredPlaintext) == 'en': #check for english
        if guess_language(decipheredPlaintext) == 'en': #check for english
            print(' > Potential plaintext no.' + str(i) + ' using 2-byte key: 1a' + hex(i).replace('0x',''))
            print(decipheredPlaintext + '\n')
    #reset to blank for next iteration
    plaintext2 = ''
    decipheredPlaintext = ''

print(' >Here we can see a single plaintext (no.188) that reads in english using the hexadecimal key of 0x1abc')
print(' >The plaintext reads:')
decipheredPlaintext = 'In ancient Egypt servants were smeared with honey to attract flies away from the pharaoh'
theKey = '0x1abc'
print(colored(decipheredPlaintext + '\n','red'))

exportSolution(decipheredPlaintext, theKey)
