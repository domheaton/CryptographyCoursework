# Author: Dominic Heaton
# Solution Script for Q3
#################################################################################
from langdetect import detect
from guess_language import guess_language
from termcolor import colored
import re
import matplotlib.pylab as plt
import itertools
import os

def loadFile():
    open_file = open("q3.txt", "r")
    ciphertext = open_file.read().rstrip('\n')
    open_file.close()
    # print(ciphertext)
    return ciphertext

def removeOldExport():
    try:
        os.remove('q3-plaintexts.txt')
    except OSError:
        pass

def findFactors(value):
    factors = []
    for i in range(1, value+1):
        if value % i == 0:
            factors.append(i)
    return factors

def removeSmallKeys(keyLengths):
    print(' >Ignoring keys < 3 in length as they are highly unlikely')
    keyLengths.remove(1)
    keyLengths.remove(2)
    return keyLengths

def letterFrequency(ct):
    ct = ct.upper() #make all upper case
    freqAlphabet = {'A' : ct.count('A'), 'B' : ct.count('B'), 'C' : ct.count('C'),
                    'D' : ct.count('D'), 'E' : ct.count('E'), 'F' : ct.count('F'),
                    'G' : ct.count('G'), 'H' : ct.count('H'), 'I' : ct.count('I'),
                    'J' : ct.count('J'), 'K' : ct.count('K'), 'L' : ct.count('L'),
                    'M' : ct.count('M'), 'N' : ct.count('N'), 'O' : ct.count('O'),
                    'P' : ct.count('P'), 'Q' : ct.count('Q'), 'R' : ct.count('R'),
                    'S' : ct.count('S'), 'T' : ct.count('T'), 'U' : ct.count('U'),
                    'V' : ct.count('V'), 'W' : ct.count('W'), 'X' : ct.count('X'),
                    'Y' : ct.count('Y'), 'Z' : ct.count('Z')}
    return freqAlphabet

def englishFrequency():
    freqEnglish = {'A': 8.17, 'B': 1.29, 'C': 2.78, 'D': 4.25,'E': 12.70,
                'F': 2.23, 'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15,
                'K': 0.77, 'L': 4.03,  'M': 2.41, 'N': 6.75, 'O': 7.51,
                'P': 1.93, 'Q': 0.10, 'R': 5.99, 'S': 6.33, 'T': 9.06,
                'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15, 'Y': 1.97,
                'Z': 0.07}
    return freqEnglish

def columnarDecrypt(ciphertext, likelyKeys):
    print('Columnar Decrypting...\n')
    for i in range(0, 2): #INCREASE THIS NUMBER FOR MORE ITERATIONS
        print(' >Key Length: ' + str(likelyKeys[i]))
        numberRows = int(len(ciphertext)/likelyKeys[i])
        print(' >Number of Rows: ' + str(numberRows))
        # generateMatrix(ciphertext, numberRows, likelyKeys[i])
        matrix = cipherToMatrix(ciphertext, numberRows)
        # print(matrix)
        matrix = transposeMatrix(matrix)
        # print(matrix)
        plaintextArray = matrixToPlaintext(matrix, likelyKeys[i], numberRows)
        printPlaintexts(plaintextArray, likelyKeys[i])
        # exportPlaintexts(plaintextArray, likelyKeys[i])

def cipherToMatrix(ciphertext, keyLength):
    return [ciphertext[i:i+keyLength] for i in range(0, len(ciphertext), keyLength)]

def transposeMatrix(matrix): #matrix of rows: key=3 gives a matrix of strings of length 3
    return [*zip(*matrix)]

def matrixToPlaintext(matrix, keyLength, numberRows): #matrix of columns: key=3 gives 3 strings
    plaintextArray = []
    tempList = []
    tempString = ''
    combinedList = []
    numberOfColumns = list(range(0,keyLength)) #list number of columns
    columnCombinations = list(set(itertools.permutations(numberOfColumns))) #list of all column permutations
    # print(' >Column permutations to attempt: ' + str(columnCombinations) + '\n')
    for i in range(0, len(columnCombinations)): #for iterating through column combinations list
        for j in range(0, keyLength): #for iterating through individual columns in combinations
            tempList = [row[columnCombinations[i][j]] for row in matrix] #fetch column in matrix
            tempString += ''.join(tempList) #turn column into string
            if j == (keyLength-1): #if we've got all the columns in the combination
                plaintextArray.append(tempString) #add string to plaintext array
                # print(plaintextArray)
                tempString = ''
    return plaintextArray

def printPlaintexts(plaintextArray, keyLength):
    print(' >Potential plaintexts for key length of ' + str(keyLength) + ':')
    for i in range(0, len(plaintextArray)):
        # if detect(plaintextArray[i]) == 'en': #attempt to limit output via language detection (not perfect)
            # if guess_language(plaintextArray[i]) == 'en': #attempt to limit output via language detection (not perfect)
        print('  ' + str(i+1) + '. ' + plaintextArray[i])
        exportToFile(plaintextArray[i])
    print() #blank line

def exportToFile(plaintext):
    open_file = open("q3-plaintexts.txt", "a")
    open_file.write(plaintext + '\n')
    open_file.close()

ciphertext = loadFile()
removeOldExport()
cipherLength = str(len(ciphertext))
keyLengths = findFactors(int(cipherLength))
print('\nStarting Decipher Attempt...\n')
print(' >Ciphertext: \n' + ciphertext + '\n')
print(' >Length of Ciphertext: ' + cipherLength)
print(' >Key lengths: ' + str(keyLengths) + '\n')
likelyKeys = removeSmallKeys(keyLengths)
print(' >Likely keys: ' + str(likelyKeys) + '\n')

#Frequency analysis
ciphertextFrequency = letterFrequency(ciphertext)
englishFrequency = englishFrequency()

#graphical representation of the analysis
x1, y1 = zip(*ciphertextFrequency.items())
xe, ye = zip(*englishFrequency.items())
plt.plot(x1, y1, xe, ye)
plt.title('Comparison of freqency of letters in CT (blue) and English (orange)')
plt.xlabel('letter')
plt.ylabel('frequency')
plt.show(block=False)

#Columnar Transposition Attempt
plaintext = columnarDecrypt(ciphertext, likelyKeys)
#leave as final line
# plt.show()
