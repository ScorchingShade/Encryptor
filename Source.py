'''
1) Take any password and account for which it will be valid
2) Tell whether it is good, bad or strong
3) Package it using a custom encryption Algorithm
4) Provide a key to the user
5) Decrypt a file using a key
6) Feature to store it in cloud-- Dropbox or google Drive

'''
import getpass
import random
import string
import sys
import os
import time
from time import sleep
from progress.bar import Bar
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

import getpass
import re

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

encryptor = None

class Encrypto:

    version="1.0"
    username=""
    password=""
    fileName="PASS.txt"
    Key=""

    #initialising innput for username and password, storing them in a temporary text file . In case of no encryption the text file will persist in the user's system
    def __init__(self, options):
        print("################################### WELCOME TO THE ENCRYPTOR BY AINC########################################\n\n\t\t\t\t\tThis is your own mobile vault")

        if(options != None):
            self.username=options["username"]
            self.password=options["password"]
        else:
            self.username=input("\nPlease enter the username you wish to add for encryption: \n")
            self.password=getpass.getpass("\nPlease enter the password to evaluate: \n")
        
        print("We shall now be storing your password securely in a file...initialising setup please wait..")

        f = open(self.fileName, "w+")

        #Progress bar to add a little bling
        bar = Bar('Adding to file', max=3)
        f.write('############################################### Welcome to The VAULT ##########################################')
        f.write('\n\n##########UserName##########\n' + self.username)
        f.write('\n\n##########Password##########\n' + self.password)
        for i in range(3):
            # Do some work
            sleep(1)
            bar.next()
        bar.finish()
        f.close()


    #Generate RSA KEY to allow encryption
    def RSA_gen(self, gui):
        print("\n\n**************************************Initialising Encryption*****************************************************\nBefore beginning you might want to check out the following points\n1) Encryption is a highly detailed and memory intensive process , be sure to have minimum hardware requirements before running the Encryptor.\n2) We at AINC are not responsible for any loss of data in case of loss of The Key of your encypted file.\n3) Make sure to never send The Key over internet or any media.\n")
       

        if(gui):
            bar = Bar('Generating Secure Key', max=2)
            for i in range(2):
                # Do some work
                sleep(1)
                bar.next()

            #Generating the passphrase for key pair generation
            Key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            self.Key=Key

            print("\n\nThis shall be your key that you may use for decrypting your file, keep it safe and NEVER share it with any unauthorized person/software. \n" + Key)
            bar.finish()

            R_enc_key = RSA.generate(2048)
            encrypted_key = R_enc_key.exportKey(passphrase=self.Key, pkcs=8,protection="scryptAndAES128-CBC")
            with open('my_private_rsa_key.bin','wb') as f:
                f.write(encrypted_key)
                f.close()
            with open('my_rsa_public_key.pem','wb') as f:
                f.write(R_enc_key.publickey().exportKey())
                f.close()
        else:
            choice=input("Do you want to continue? (y/n):\n")
            if choice=='y' or choice == 'Y' or choice == 'Yes' or choice == 'yes' or choice == 'YES':
                bar = Bar('Generating Secure Key', max=2)
                for i in range(2):
                    # Do some work
                    sleep(1)
                    bar.next()

                #Generating the passphrase for key pair generation
                Key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
                self.Key=Key

                print("\n\nThis shall be your key that you may use for decrypting your file, keep it safe and NEVER share it with any unauthorized person/software. \n" + Key)
                bar.finish()

                R_enc_key = RSA.generate(2048)
                encrypted_key = R_enc_key.exportKey(passphrase=self.Key, pkcs=8,protection="scryptAndAES128-CBC")
                with open('my_private_rsa_key.bin','wb') as f:
                    f.write(encrypted_key)
                    f.close()
                with open('my_rsa_public_key.pem','wb') as f:
                    f.write(R_enc_key.publickey().exportKey())
                    f.close()
            else:
                print("\nNo Problem! Let's do this again someday!")


    #A basic password evaluator to check the password strength
    def Evaluator(self):

        passw=self.password

        if len(passw) <= 6:
            print('The password must be between 6 and 12 characters.\n')
            return 1

        else:
            password_scores = {0: 'Horrible', 1: 'Weak', 2: 'Medium', 3: 'Strong'}

            password_strength = dict.fromkeys(['has_upper', 'has_lower', 'has_num'], False)
            if re.search(r'[A-Z]', passw):
                password_strength['has_upper'] = True
            if re.search(r'[a-z]', passw):
                password_strength['has_lower'] = True
            if re.search(r'[0-9]', passw):
                password_strength['has_num'] = True

            score = len([b for b in password_strength.values() if b])

            if (password_scores[score] == "Weak"):
                print(
                    "\nYour password score is: Weak!\nHere's what you should try-\n1) Ensure that your password contains atleast one capital letter.\n2) Use numbers 0-9 in your password to make it stronger! \n3) Use symbols where possible to make it even more credible\n")

            elif (password_scores[score] == "Medium"):
                print(
                    "\nYour password score is: Good Enough!\nYou already have a decent password score, try the following to get even better rating!-\n1) Ensure that your password contains atleast one capital letter.\n2) Use numbers 0-9 in your password to make it stronger! \n3) Use symbols where possible to make it even more credible\n")

            else:
                print(
                    "\nYour password score is: Awesome!\nThis password activates god mode! Congrats you are protected!\nDon't forget to change your password regularly to prevent any hacks!\n")

    #Encryption using AES OAEP
    def encrypt(self, path):
        # the chunksize is basically the amount of data being read at a time
        chunksize=64*1024
        if(path != None):
            pub_key = path
        else:
            pub_key=input("Enter the path to your public key:(e.g /home/pub_key.pem)\n")
        
        with open('PASS.txt','rb') as infile:
            with open('AINC_encrypted_File.bin','wb') as outfile:
                recipient_key = RSA.import_key(
                    open(pub_key).read())
                #IN OAEP we have to generate a random string to fill in the encryption, we have used a 16 byte string here
                session_key = get_random_bytes(16)

                #Cipher will be used to encrypt the data using the public key.
                cipher_rsa = PKCS1_OAEP.new(recipient_key)
                outfile.write(cipher_rsa.encrypt(session_key))

                cipher_aes = AES.new(session_key, AES.MODE_EAX)

                #reading the text file as a chunk of bytes at a time and allowing encryption for the same
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)

                    ciphertext, tag = cipher_aes.encrypt_and_digest(chunk)

                    outfile.write(cipher_aes.nonce)
                    outfile.write(tag)
                    outfile.write(ciphertext)

                    
                    bar = Bar('Encrypting File', max=2)
                    for i in range(2):
                        # Do some work
                        sleep(1)
                        bar.next()
                    bar.finish()
                    print("Successfully completed encrypting the file!")
                
                infile.close()
                outfile.close()
                os.remove("PASS.txt")


    #Decrypting the data
    def decrypt(self, path):
        if(path != None):
            with open(path, 'rb') as key_file:
                Key = key_file.read()
                key_file.close()
        else:
            Key=input("Enter your secret Key:\n")
        with open('AINC_encrypted_File.bin','rb') as fobj:
            with open('decrypted.txt','wb') as outfile:
                private_key= RSA.import_key(open('my_private_rsa_key.bin').read(),passphrase=Key)
                enc_session_key, nonce, tag, ciphertext = [fobj.read(x)
                                                           for x in (private_key.size_in_bytes(),
                                                                     16, 16, -1)]

                cipher_rsa = PKCS1_OAEP.new(private_key)
                session_key = cipher_rsa.decrypt(enc_session_key)
                cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)

                data=cipher_aes.decrypt_and_verify(ciphertext, tag)

                #check whether dencryption is done properly or not
                #print(data)
                outfile.write(data)

                bar = Bar('Decrypting File', max=2)
                for i in range(2):
                    # Do some work
                    sleep(1)
                    bar.next()
                bar.finish()
                print("Successfully completed Decrypting the file!")

        fobj.close()
        outfile.close()


def options(choice):
    if(choice==1):
        encryptor.Evaluator()
    elif(choice==2):
        select_encrypt()
    elif(choice==3):
        select_decrypt()
    elif(choice==4):
        encryptor.RSA_gen(True)
    elif(choice==5):
        print("\nThank you for using the Encryptor by AINC! Hope to see you soon!")
        exit(1)
    else:
        print("Wrong input, please enter again!")

def set_encrypto(options):
    global encryptor
    encryptor = Encrypto(options)

def select_encrypt():
    filetypes = (
        ('All files', '*.*'),
        ('text files', '*.txt')
    )

    selected_file = fd.askopenfilename(
        title='Select a file',
        initialdir='/',
        filetypes=filetypes)

    encryptor.encrypt(selected_file)

def select_decrypt():
    filetypes = (
        ('All files', '*.*'),
        ('text files', '*.txt')
    )

    selected_file = fd.askopenfilename(
        title='Select a file',
        initialdir='/',
        filetypes=filetypes)

    encryptor.decrypt(selected_file)

if __name__== "__main__":
    # Setup window
    window = tk.Tk()
    window.title("Encryptor")
    window.geometry('400x400')

    tk.Label(window, text="Username: ").grid(row=1, column=0)
    username_field = tk.Entry(window)
    username_field.grid(row=1, column=1)

    tk.Label(window, text="Password: ").grid(row=2, column=0)
    password_field = tk.Entry(window)
    password_field.grid(row=2, column=1)

    submit_button = ttk.Button(
        window,
        text='Submit',
        command=lambda: set_encrypto({"username":username_field.get(), "password":password_field.get()})
    )

    submit_button.grid(row=3, column=1)

    tk.Label(window, text="Options:").grid(row=5, column=0)

    # Appraise Password
    appraise_button = ttk.Button(
        window,
        text='Appraise Password',
        command=lambda: options(1)
    )

    appraise_button.grid(row=6, column=0)

    # Encrypt Username and Password
    encrypt_button = ttk.Button(
        window,
        text='Encrypt Username and Password',
        command=lambda: options(2)
    )

    encrypt_button.grid(row=7, column=0)

    # Decrypt an existing file
    decrypt_button = ttk.Button(
        window,
        text='Decrypt file',
        command=lambda: options(3)
    )

    decrypt_button.grid(row=8, column=0)

    # Generate Key Pair
    generate_key_pair_button = ttk.Button(
        window,
        text='Generate Key Pair',
        command=lambda: options(4)
    )

    generate_key_pair_button.grid(row=9, column=0)

    # Quit
    quit_button = ttk.Button(
        window,
        text='Quit',
        command=lambda: options(5)
    )

    quit_button.grid(row=10, column=0)



    submit_button.grid(row=3, column=1)


    window.mainloop()

