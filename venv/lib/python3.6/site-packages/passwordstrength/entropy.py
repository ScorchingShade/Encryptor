import string
import yaml
import math

from passwordstrength.dir import database_path


class Entropy:
    def __init__(self):
        with open(database_path('google-10000-english.txt')) as f:
            self.common_words = f.read().strip().split('\n')
        with open(database_path('words.txt')) as f:
            self.dictionary_words = set(f.read().strip().split('\n')) - set(self.common_words)
        with open(database_path('leetspeak.yaml')) as f:
            self.leet = yaml.safe_load(f)['min']

    def entropy_brute_force(self, password):
        entropy = 1
        for i, char in enumerate(password):
            if char in string.punctuation + string.digits:
                entropy *= len(string.printable)
            elif self._consecutive(password, i):
                entropy *= len(string.ascii_lowercase)
            else:
                entropy *= len(string.ascii_letters)

        return entropy

    @staticmethod
    def _consecutive(password, index):
        if len(password) < index+3:
            return False

        if all([char.islower() for char in password[index:index+3]]):
            return True
        elif all([char.isupper() for char in password[index:index+3]]):
            return True
        else:
            return False

    def entropy_dictionary_attack(self, password):
        entropy = 1
        if password.lower() in self.common_words:
            entropy *= self.common_words.index(password)
        elif password.lower() in self.common_words:
            entropy *= 2*len(self.common_words)
        elif password.lower() in self.dictionary_words:
            entropy *= len(self.dictionary_words)
        else:
            return math.inf

        return self.word_difficulty(password)*entropy

    def word_difficulty(self, word):
        if word.islower():
            return 1
        elif word[0].isupper():
            return 2
        elif word.isupper():
            return 3
        elif word.isalpha():
            return pow(2, len(word))
        else:
            difficulty = 1
            for char in word:
                difficulty *= 2 + len(self.leet.get(char, []))
            return difficulty

    def entropy_diceware(self, password):
        entropy = 1
        start_word = 0
        for i, char in enumerate(password):
            if start_word >= len(password):
                break
            if password[start_word:i+1] in self.common_words:
                word = password[start_word:i+1]
                entropy *= self.word_difficulty(word)*self.common_words.index(word)
                start_word = i+1
            elif password[start_word:i+1] in self.dictionary_words:
                word = password[start_word:i + 1]
                entropy *= self.word_difficulty(word)*len(self.dictionary_words)
                start_word = i+1
        if start_word < len(password):
            entropy *= self.entropy_brute_force(password[start_word:])

        return entropy

    def entropy(self, password):
        return self.entropy_worst_case(password)

    def log_entropy(self, password):
        return math.log2(self.entropy(password))

    def entropy_worst_case(self, password):
        return min(self.entropy_brute_force(password),
                   self.entropy_dictionary_attack(password),
                   self.entropy_diceware(password))
