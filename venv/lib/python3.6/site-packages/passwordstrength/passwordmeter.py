# based on http://www.passwordmeter.com
import string
# import math

class PasswordStrength:
    def __init__(self, password):
        self.password = password
        self.total_score = 0
        self.seqSymbols = r'!"#$%&\'()*,.:;<=><>=<?@[]^_`|~{}/\/+-+'
        self.active_rules = {
            'Additions': [
                'nLengthBonus',
                'nAlphaUCBonus',
                'nAlphaLCBonus',
                'nNumberBonus',
                'nSymbolBonus',
                'nMidCharBonus'
            ],
            'Deductions': [
                'nAlphasOnlyBonus',
                'nNumbersOnlyBonus',
                'nRepCharBonus',
                'nConsecAlphaUCBonus',
                'nConsecAlphaLCBonus',
                'nConsecNumberBonus',
                'nSeqAlphaBonus',
                'nSeqNumberBonus',
                'nSeqSymbolBonus'
            ]
        }
        self._rule_scores = {
            'Additions': {
                'nLengthBonus': 0,
                'nAlphaUCBonus': 0,
                'nAlphaLCBonus': 0,
                'nNumberBonus': 0,
                'nSymbolBonus': 0,
                'nMidCharBonus': 0
            },
            'Deductions': {
                'nAlphasOnlyBonus': 0,
                'nNumbersOnlyBonus': 0,
                'nRepCharBonus': 0,
                'nConsecAlphaUCBonus': 0,
                'nConsecAlphaLCBonus': 0,
                'nConsecNumberBonus': 0,
                'nSeqAlphaBonus': 0,
                'nSeqNumberBonus': 0,
                'nSeqSymbolBonus': 0
            }
        }

    def strength(self):
        self.total_score = 0
        self.rule_scores()
        for rule_type, rule_list in self.active_rules.items():
            if rule_type == 'Additions':
                for rule in rule_list:
                    self.total_score += self._rule_scores[rule_type][rule]
            elif rule_type == 'Deductions':
                for rule in rule_list:
                    self.total_score -= self._rule_scores[rule_type][rule]
            else:
                raise IndexError('Invalid rule_type: {}'.format(rule_type))
        return self.total_score

    def rule_scores(self):
        Additions = self.Additions(self.password)
        Deductions = self.Deductions(self.password, self.seqSymbols)

        for rule_type, rule_list in self._rule_scores.items():
            for rule, rule_score in rule_list.items():
                self._rule_scores[rule_type][rule] = 1

        for rule_type, rule_list in self._rule_scores.items():
            if rule_type == 'Additions':
                for rule, rule_score in rule_list.items():
                    if rule == 'nLengthBonus':
                        self._rule_scores[rule_type][rule] = Additions.nLengthBonus()
                    elif rule == 'nAlphaUCBonus':
                        self._rule_scores[rule_type][rule] = Additions.nAlphaUCBonus()
                    elif rule == 'nAlphaLCBonus':
                        self._rule_scores[rule_type][rule] = Additions.nAlphaLCBonus()
                    elif rule == 'nNumberBonus':
                        self._rule_scores[rule_type][rule] = Additions.nNumberBonus()
                    elif rule == 'nSymbolBonus':
                        self._rule_scores[rule_type][rule] = Additions.nSymbolBonus()
                    elif rule == 'nMidCharBonus':
                        self._rule_scores[rule_type][rule] = Additions.nMidCharBonus()
                    else:
                        raise IndexError('Invalid rule: {}'.format(rule))
            elif rule_type == 'Deductions':
                for rule in rule_list:
                    if rule == 'nAlphasOnlyBonus':
                        self._rule_scores[rule_type][rule] = Deductions.nAlphasOnlyBonus()
                    elif rule == 'nNumbersOnlyBonus':
                        self._rule_scores[rule_type][rule] = Deductions.nNumbersOnlyBonus()
                    elif rule == 'nRepCharBonus':
                        self._rule_scores[rule_type][rule] = Deductions.nRepCharBonus()
                    elif rule == 'nConsecAlphaUCBonus':
                        self._rule_scores[rule_type][rule] = Deductions.nConsecAlphaUCBonus()
                    elif rule == 'nConsecAlphaLCBonus':
                        self._rule_scores[rule_type][rule] = Deductions.nConsecAlphaLCBonus()
                    elif rule == 'nConsecNumberBonus':
                        self._rule_scores[rule_type][rule] = Deductions.nConsecNumberBonus()
                    elif rule == 'nSeqAlphaBonus':
                        self._rule_scores[rule_type][rule] = Deductions.nSeqAlphaBonus()
                    elif rule == 'nSeqNumberBonus':
                        self._rule_scores[rule_type][rule] = Deductions.nSeqNumberBonus()
                    elif rule == 'nSeqSymbolBonus':
                        self._rule_scores[rule_type][rule] = Deductions.nSeqSymbolBonus()
                    else:
                        raise IndexError('Invalid rule: {}'.format(rule))
            else:
                raise IndexError('Invalid rule_type: {}'.format(rule_type))

        return self._rule_scores

    def rating(self):
        score = self.strength()
        if score in range(0, 20):
            return "Very Weak"
        elif score in range(20, 40):
            return "Weak"
        elif score in range(40, 60):
            return "Good"
        elif score in range(60, 80):
            return "Strong"
        elif score >= 80:
            return "Very Strong"
        else:
            raise ValueError('Value error')

    class Additions:
        def __init__(self, password):
            self.password = password

        def nLengthBonus(self):
            return len(self.password) * 4

        def nAlphaUCBonus(self):
            password = self.password
            nUC = PasswordStrength._count(password, string.ascii_uppercase)
            if nUC in range(1, len(password)):
                return (len(password)-nUC) * 2
            else:
                return 0

        def nAlphaLCBonus(self):
            password = self.password
            nLC = PasswordStrength._count(password, string.ascii_uppercase)
            if nLC in range(1, len(password)):
                return (len(password) - nLC) * 2
            else:
                return 0

        def nNumberBonus(self):
            nNumber = PasswordStrength._count(self.password, string.digits)
            return nNumber * 4

        def nSymbolBonus(self):
            nSymbol = PasswordStrength._count(self.password, string.punctuation)
            return nSymbol * 6

        def nMidCharBonus(self):
            password = self.password
            nMidChar = 0
            for i, char in enumerate(password):
                if i != 0 and i != len(password)-1:
                    if char in string.digits + string.punctuation:
                        nMidChar += 1
            return nMidChar * 2

    class Deductions:
        def __init__(self, password, seqSymbols):
            self.password = password
            self.seqSymbols = seqSymbols

        def nAlphasOnlyBonus(self):
            def alphasOnly():
                for char in self.password:
                    if char in string.digits:
                        return False
                return True

            if alphasOnly():
                return len(self.password)
            else:
                return 0

        def nNumbersOnlyBonus(self):
            def numbersOnly():
                for char in self.password:
                    if char in string.ascii_letters:
                        return False
                return True

            if numbersOnly():
                return len(self.password)
            else:
                return 0

        def nRepCharBonus(self):
            nRepInc = 0
            temp_char = ''
            for char in sorted(self.password):
                if temp_char:
                    if char == temp_char:
                        nRepInc += 1
                temp_char = char
            return nRepInc

        def nConsecAlphaUCBonus(self):
            nConsecAlphaUC = PasswordStrength._count_conseq(self.password, string.ascii_uppercase)
            return nConsecAlphaUC * 2

        def nConsecAlphaLCBonus(self):
            nConsecAlphaLC = PasswordStrength._count_conseq(self.password, string.ascii_lowercase)
            return nConsecAlphaLC * 2

        def nConsecNumberBonus(self):
            nConsecNumber = PasswordStrength._count_conseq(self.password, string.digits)
            return nConsecNumber * 2

        def nSeqAlphaBonus(self):
            nSeqAlpha = PasswordStrength._count_seq(self.password.lower(), string.ascii_lowercase)
            return nSeqAlpha * 3

        def nSeqNumberBonus(self):
            nSeqNumber = PasswordStrength._count_seq(self.password, string.digits + '0')
            return nSeqNumber * 3

        def nSeqSymbolBonus(self):
            password = self.password
            nSeqSymbol = PasswordStrength._count_seq(password, self.seqSymbols)
            return nSeqSymbol * 3

    @staticmethod
    def _count(password, rule_string):
        n = 0
        for char in password:
            if char in rule_string:
                n += 1
        return n

    @staticmethod
    def _count_conseq(password, rule_string):
        temp_char = ''
        n = 0
        for char in password:
            if char in rule_string:
                if temp_char:
                    if temp_char in rule_string:
                        n += 1
                temp_char = char
        return n

    @staticmethod
    def _count_seq(password, rule_string):
        n = 0
        for i in range(len(rule_string) - 3):
            sFwd = chr(ord(rule_string[0]) + i) \
                   + chr(ord(rule_string[0]) + i + 1) \
                   + chr(ord(rule_string[0]) + i + 2)
            sRev = sFwd[::-1]
            if sFwd in password or sRev in password:
                n += 1
        return n


if __name__ == '__main__':
    # print(PasswordStrength('password').strength())
    # print(PasswordStrength('password').rule_scores())
    pass
