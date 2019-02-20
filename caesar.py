# Author: Dominic Heaton
# Caeser Cipher Brute Force
# Tries 25 shifts of the alphabet to solve the CT
##################################################
from langdetect import detect
from guess_language import guess_language
from termcolor import colored

def encrypt(string, shift):
  cipher = ''
  for char in string: #Check spaces
    if char == ' ':
      cipher = cipher + char
    elif  char.isupper(): #Upper case shift
      cipher = cipher + chr((ord(char) + shift - 65) % 26 + 65)
    else: #Lower case shift
      cipher = cipher + chr((ord(char) + shift - 97) % 26 + 97)
  return cipher

def caeserDecrypt():
    print('\nAttempting Caeser Cipher Brute Force')
    print(' >ciphertext: ' + ciphertext)
    for i in range(0,26):
        decrypted_shift = encrypt(ciphertext, i)
        # if detect(decrypted_shift) == 'en': #attempt to limit output via language detection (not perfect)
            # if guess_language(decrypted_shift) == 'en': #attempt to limit output via language detection (not perfect)
        print(' >plaintext : ' + colored(decrypted_shift, 'red')) #print in colour
        print(' >shift num.: ' + str(i-26) + '\n')
    print('Finished Caeser Decrypt Attempt')

### Main Program ###
open_file = open("q1.txt", "r")
ciphertext = open_file.read().rstrip('\n')
ciphertext = ciphertext.rstrip('.')
open_file.close()

caeserDecrypt()
