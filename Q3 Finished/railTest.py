# Author: Dominic Heaton
# Rail Fence Transpoition Cipher Test Script
#   Encrypts message 'thisisatestoftherailfencedecoder' using max number of
#   possible rails for length of the message
#   Decrypts the ciphertest also to show it can be returned to original text
#################################################################################
from langdetect import detect
from guess_language import guess_language
from termcolor import colored
import re
import matplotlib.pylab as plt

def findFactors(value):
    factors = []
    for i in range(1, value+1):
        if value % i == 0:
            factors.append(i)
    return factors

def railEncrypt(plaintext, numberOfRails):
    #generate matrix
    railMatrix = []
    for i in range(numberOfRails):
        railMatrix.append([])
    for row in range(numberOfRails):
        for column in range(len(plaintext)):
            railMatrix[row].append('.')

    #assign plaintext to matrix
    row = 0
    check = 0
    for i in range(len(plaintext)):
        if check == 0:
            railMatrix[row][i] = plaintext[i]
            row += 1
        if row == numberOfRails:
            check = 1
            row -= 1
        elif check == 1:
            row -= 1
            railMatrix[row][i] = plaintext[i]
            if row == 0:
                check = 0
                row = 1

    #form ciphertext from matrix
    ciphertext = ''
    for i in range(numberOfRails):
        for j in range(len(plaintext)):
            ciphertext += railMatrix[i][j]
    ciphertext = re.sub(r"\.","",ciphertext)
    return ciphertext

def railDecrypt(ciphertext, numberOfRails):
    #generate matrix
    railMatrix = []
    for i in range(numberOfRails):
        railMatrix.append([])
    for row in range(numberOfRails):
        for column in range(len(ciphertext)):
            railMatrix[row].append('.')

    #assign ciphertext to matrix
    row = 0
    check = 0
    for i in range(len(ciphertext)):
        if check == 0:
            railMatrix[row][i] = ciphertext[i]
            row += 1
            if row == numberOfRails:
                check = 1
                row -= 1
        elif check == 1:
            row -= 1
            railMatrix[row][i] = ciphertext[i]
            if row == 0:
                check = 0
                row = 1

    #sort matrix
    value = 0
    for i in range(numberOfRails):
        for j in range(len(ciphertext)):
            tempVal = railMatrix[i][j]
            if re.search("\\.", tempVal):
                continue
            else:
                railMatrix[i][j] = ciphertext[value]
                value += 1

    #form plaintext from matrix
    check = 0
    row = 0
    plaintext = ''
    for i in range(len(ciphertext)):
        if check == 0:
            plaintext += railMatrix[row][i]
            row += 1
            if row == numberOfRails:
                check = 1
                row -= 1
        elif check == 1:
            row -=1
            plaintext += railMatrix[row][i]
            if row == 0:
                check = 0
                row = 1
    plaintext = re.sub(r"\.","",plaintext)
    return plaintext

msg = 'thisisatestoftherailfencedecoder'
msgLength = str(len(msg))
keyLengths = str(findFactors(int(msgLength)))
print('\nStarting Rail Fence Decipher Attempt...\n')
print(' >Message: \n' + msg + '\n')
print(' >Length of Ciphertext: ' + msgLength)
maxNumberOfRails = str(int(msgLength)-1)
print(' >Max number of Rails is therefore: ' + maxNumberOfRails + '\n') #max rail number is one less than length of text

#brute force to show encrypted and decrypted for max number of rails possible for length of message
for numberOfRails in range(2, int(maxNumberOfRails)+1):
    print(' >No. of Rails: ' + str(numberOfRails))
    ciphertext = railEncrypt(msg, numberOfRails)
    print(' >Ciphertext: ' + ciphertext)
    plaintext = railDecrypt(ciphertext, numberOfRails)
    print(' >Plaintext: ' + plaintext + '\n')
