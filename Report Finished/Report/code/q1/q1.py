# Author: Dominic Heaton
# Solution Script for Q1
# Performs Kasisky Test and Frequency Analysis to establish key length and
#   to decipher the final plaintext message which is exported in q1-solution.txt
# REQUIREMENTS: See libraries imported;
#   langdetect, guess-language, termcolor, re, matplotlib
#################################################################################
from langdetect import detect
from guess_language import guess_language
from termcolor import colored
import re
import matplotlib.pylab as plt

def loadFile():
    open_file = open("q1.txt", "r")
    ciphertext = open_file.read().rstrip('\n')
    open_file.close()
    # print(ciphertext)
    return ciphertext

def stripPunctuation(ciphertext):
    noPunctuation = re.sub(r'[^\w\s]','',ciphertext) #remove all non-alphanumerics
    strippedCiphertext = noPunctuation.replace(' ', '') #remove all spaces
    return strippedCiphertext

def largestPattern(ciphertext):
    length = 0
    i=0
    j=0
    for j in range(len(ciphertext)):
        for i in range(len(ciphertext)):
            substring = ciphertext[j:i]
            if len(list(re.finditer(re.escape(substring),ciphertext))) > 1  and len(substring) > length:
                match = substring
                length = len(substring)
    return match.strip() #remove all spaces

def repeatDistance(ciphertext, repeatedString, stringLength):
    firstOccurance = ciphertext.find(repeatedString) #start of firstOccurance
    endOfFirstOccurance = firstOccurance + stringLength #end of firstOccurance
    secondOccurance = ciphertext.find(repeatedString, endOfFirstOccurance) #start finding after firstOccurance
    repeatDistance = secondOccurance - firstOccurance
    return repeatDistance

def findFactors(value):
    factors = []
    for i in range(1, value+1):
        if value % i == 0:
            factors.append(i)
    return factors

def removeSmallKeys(factors):
    print(' >Ignoring keys < 3 in length as they are highly unlikely')
    factors.remove(1)
    factors.remove(2)
    return factors

#function returns three sets of characters - each set has been encrypted with the same letter of the key
def getEncryptedGroups(ciphertext, keyLength):
    keyLetter1 = ''
    keyLetter2 = ''
    keyLetter3 = ''
    for i in range(0,len(ciphertext), keyLength):
        keyLetter1 += ciphertext[i]
    for j in range(1,len(ciphertext), keyLength):
        keyLetter2 += ciphertext[j]
    for k in range(2,len(ciphertext), keyLength):
        keyLetter3 += ciphertext[k]
    return keyLetter1, keyLetter2, keyLetter3

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

def englishFrequency(): #from wikipedia
    freqEnglish = {'A': 8.17, 'B': 1.29, 'C': 2.78, 'D': 4.25,'E': 12.70,
                'F': 2.23, 'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15,
                'K': 0.77, 'L': 4.03,  'M': 2.41, 'N': 6.75, 'O': 7.51,
                'P': 1.93, 'Q': 0.10, 'R': 5.99, 'S': 6.33, 'T': 9.06,
                'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15, 'Y': 1.97,
                'Z': 0.07}
    return freqEnglish

def maxValKey(dictionary):
    return max(dictionary, key=dictionary.get)

def mostFrequent(frequency1, frequency2, frequency3, englishFrequency):
    mostFrequent1 = maxValKey(frequency1) #most frequent character in ciphertext for 1st key letter
    mostFrequent2 = maxValKey(frequency2) #most frequent character in ciphertext for 2nd key letter
    mostFrequent3 = maxValKey(frequency3) #most frequent character in ciphertext for 3rd key letter
    mostFrequentEnglish = maxValKey(englishFrequency) #most frequent character in ciphertext for 3rd key letter
    return mostFrequent1, mostFrequent2, mostFrequent3, mostFrequentEnglish

def findShift(mostFrequent1, mostFrequent2, mostFrequent3, mostFrequentEnglish):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # +1 due to indexing from 0
    position1 = alphabet.find(mostFrequent1) + 1
    position2 = alphabet.find(mostFrequent2) + 1
    position3 = alphabet.find(mostFrequent3) + 1
    positionAlphabet = alphabet.find(mostFrequentEnglish) + 1
    shift1 = positionAlphabet - position1
    shift2 = positionAlphabet - position2
    shift3 = positionAlphabet - position3
    return shift1, shift2, shift3

def caeserShift(string, shift):
  cipher = ''
  for char in string: #Check spaces
    if char == ' ':
      cipher = cipher + char
    elif  char.isupper(): #Upper case shift
      cipher = cipher + chr((ord(char) + shift - 65) % 26 + 65)
    else: #Lower case shift
      cipher = cipher + chr((ord(char) + shift - 97) % 26 + 97)
  return cipher

#rebuild words
def rebuildPlaintext(shifted1, shifted2, shifted3):
    plaintext = ''
    for i in range(0, len(shifted1)):
      plaintext += shifted1[i]
      plaintext += shifted2[i]
      plaintext += shifted3[i]
    return plaintext

def removeKey(dictionary, key):
    del dictionary[key]

def nextMostFrequent(frequency3):
    mostFrequent3 = maxValKey(frequency3) #find most frequent
    removeKey(frequency3, mostFrequent3) #remove most frequent (we know it didnt work)
    nextMostFrequentVal = maxValKey(frequency3) #get the next most frequent
    return nextMostFrequentVal

def findShift3(nextMostFrequentVal, mostFrequentEnglish):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    position3 = alphabet.find(nextMostFrequentVal) + 1
    positionAlphabet = alphabet.find(mostFrequentEnglish) + 1
    newShift3 = positionAlphabet - position3
    return newShift3

def findKey(shift1, shift2, shift3):
    reversed = 'ZYXWVUTSRQPONMLKJIHGFEDCBA' #reversed as keys have been calculated from that perspective (handles minus [-] signs)
    theKey = ''
    theKey += reversed[shift1-1]
    theKey += reversed[shift2-1]
    theKey += reversed[shift3-1]
    return theKey.lower() #lowercase

def exportSolution(punctuatedPlaintext, theKey):
    open_file = open("q1-solution.txt", "w")
    open_file.write('Plaintext: ' + punctuatedPlaintext + '\n\nKey: ' + theKey)
    open_file.close()

### MAIN PROGRAM
ciphertext = loadFile()
print('\nStarting Vigenere Decipher Attempt...\n')
print(' >Ciphertext: \n' + ciphertext + '\n')

# START KASISKY TEST
ciphertext = stripPunctuation(ciphertext)
print(' >Removing spaces and punctuation: \n' + ciphertext + '\n')

print(' >Calculating...\n')

largestRepeatedPattern = largestPattern(ciphertext)
print(' >Largest repeated string: ' + largestRepeatedPattern)

stringLength = len(largestRepeatedPattern)
print(' >Length of repeated string: ' + str(stringLength))

distanceBetweenRepetitions = repeatDistance(ciphertext, largestRepeatedPattern, stringLength)
print(' >Distance between repetitions: ' + str(distanceBetweenRepetitions))

factors = findFactors(distanceBetweenRepetitions)
# print(' >Possible key lengths: ' + colored(str(factors), 'red'))
print(' >Possible key lengths: ' + str(factors))

likelyKeys = removeSmallKeys(factors)
print(' >Likely keys: ' + str(likelyKeys))
print(' >Attempt frequency analysis with key space of ' + str(likelyKeys[0]))
print(' >Move to next key space listed if it fails')
#END OF KASISKY TEST

#Attempting first likely keylength (i.e. 3)
keyLength = 3
keyLetter1, keyLetter2, keyLetter3 = getEncryptedGroups(ciphertext, keyLength)
# print(keyLetter1)
# print(keyLetter2)
# print(keyLetter3)

#Frequency analysis
frequency1 = letterFrequency(keyLetter1)
frequency2 = letterFrequency(keyLetter2)
frequency3 = letterFrequency(keyLetter3)
englishFrequency = englishFrequency()

#graphical representation of the analysis
x1, y1 = zip(*frequency1.items())
x2, y2 = zip(*frequency2.items())
x3, y3 = zip(*frequency3.items())
xe, ye = zip(*englishFrequency.items())
plt.subplot(3,1,1)
plt.plot(x1, y1, xe, ye)
plt.title('Comparison of freqency of letters in CT (blue) and English (orange)')
plt.ylabel('frequency')
plt.subplot(3,1,2)
plt.plot(x2, y2, xe, ye)
plt.ylabel('frequency')
plt.subplot(3,1,3)
plt.plot(x3, y3, xe, ye)
plt.xlabel('letter')
plt.ylabel('frequency')
plt.show(block=False) #prevents the graph from plotting here to stop blocking of program

#find most frequent values
mostFrequent1, mostFrequent2, mostFrequent3, mostFrequentEnglish = mostFrequent(frequency1, frequency2, frequency3, englishFrequency)

#examine the shift amounts
shift1, shift2, shift3 = findShift(mostFrequent1, mostFrequent2, mostFrequent3, mostFrequentEnglish)
# print(shift1)
# print(shift2)
# print(shift3)

#shift
shifted1 = caeserShift(keyLetter1, shift1)
shifted2 = caeserShift(keyLetter2, shift2)
shifted3 = caeserShift(keyLetter3, shift3)
# print(shifted1)
# print(shifted2)
# print(shifted3)

#get plaintext
plaintext = rebuildPlaintext(shifted1, shifted2, shifted3)
print('\n >Plaintext Decipher Attempt Produces:\n' + plaintext)
print(' >This is close to resembling english but every third letter is not quite right')

#find the next most frequent value and therefore shift for the 3rd set of letters
nextMostFrequentVal = nextMostFrequent(frequency3)
newShift3 = findShift3(nextMostFrequentVal, mostFrequentEnglish)
newShifted3 = caeserShift(keyLetter3, newShift3)

#finally rebuild the cipher to show the final rebuildPlaintext
plaintext = rebuildPlaintext(shifted1, shifted2, newShifted3)
print('\n >2nd attempt to decipher gives:\n' + plaintext)
print(' >This is now an english sentence, just requiring the spaces and punctuation to be re-entered\n')
# manual addition of punctuation through inspection of the ciphertext
punctuatedPlaintext = 'Formative assessment can be viewed as a mean to enhance the learning process. Based on the results of such assessments, students will be able to assess their knowledge and identify strengths and weaknesses. The teacher will also have indication on how well the students are grasping the fundamental facts and whether he needs to alter their teaching to emphasis some important concepts.'
print(' >Formatting this as shown in the original Ciphertext gives:\n' + punctuatedPlaintext + '\n')

print(' >The key is therefore of length 3. The shifts used to decipher the text allows the key to be recovered as displayed below')
theKey = findKey(shift1, shift2, newShift3)
print(' >Key: ' + theKey + '\n')

exportSolution(punctuatedPlaintext, theKey)

#leave as last line to show the graphs
plt.show()
