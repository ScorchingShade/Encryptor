from __future__ import print_function


def get_strong_password(password_checker, passing_score=70):
    loop = True
    password = input('Enter your password:')
    while True:
        try:
            checker = password_checker(password)
            print(checker.rating())
            if checker.strength() > passing_score:
                print('Your password passed the minimum score.')
                while True:
                    yesno = input('Do you want to enter a new password? [y/n]')
                    if yesno == 'y':
                        break
                    elif yesno == 'n':
                        loop = False
                        break
            if not loop:
                break
            print('Your password passed the minimum score.')
            password = input('Please enter a new password.')
        except KeyboardInterrupt:
            break
