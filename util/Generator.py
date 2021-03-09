import random

class Generator:
    def __init__(self):
        #No space char
        self.all_charactors = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ';', ':', '\'', '"', ',', '<', '>', '.', '/', '?', '[', ']', '{', '}', '\\', '|', '-', '_', '+', '='
        ]

    def random_char(self, list_of_chars):
        return random.choice(list_of_chars)

    def generate_password(self, char_length):
        random_password = ''
        if char_length <=0:
            raise SystemExit(1)
        
        while(char_length > 0):
            random_password += self.random_char(self.all_charactors)
            char_length -= 1

        return random_password
