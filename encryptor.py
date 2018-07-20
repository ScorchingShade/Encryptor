'''
1) Take any password and account for which it will be valid
2) Tell whether it is good, bad or strong
3) Package it using a custom encryption Algorithm
4) Provide a key to the user
5) Decrypt a file using a key
6) Feature to store it in cloud-- Dropbox or google Drive
'''
import getpass
import re
import passwordmeter

class Encrypto:

    def __password(self, password_str):
        while True:
            if len(password_str) <= 6:
                print('The password must be between 6 and 12 characters.\n')
                break
        password_scores = {0: 'Horrible', 1: 'Weak', 2: 'Medium', 3: 'Strong'}

        password_strength = dict.fromkeys(['has_upper',
                                           'has_lower',
                                           'has_num'],
                                          False)

        if re.search(r'[A-Z]', password_str):
            password_strength['has_upper'] = True
        if re.search(r'[a-z]', password_str):
            password_strength['has_lower'] = True
        if re.search(r'[0-9]', password_str):
            password_strength['has_num'] = True

        score = len([b for b in password_strength.values() if b])

        print('Password is %s' % password_scores[score])

    def _input_(self):
        user_id = input('\nEnter the account name/User id for which you want the password to be made:\n')
        user_pass = getpass.getpass('\nEnter the password you wish to test:\n')
        print('Password entered:', user_pass)
        Encrypto.__password(Encrypto, user_pass)

Encrypto._input_(Encrypto)
