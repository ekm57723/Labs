#Lab 3 

#Defining the class for the Ceasar Cypher object
class CaesarCipher:
    def __init__(self, shift = 2):
        self.shift = shift
        self.letters = 'abcdefghijklmnopqrstuvwxyz'
        self.special = "~!@#$%^&*()_+={}[]|:;'<>,.?/"
    
    #Encrypting text with shift by -2, also converting all upper case inputs to lower case
    def encryption(self, text):
        text = text.lower()
        return ''.join(self._shift_char(x, self.shift) for x in text)
    
    #Decrypting text by +2 shift, also ensuring all letter inputs are lowercase
    def decryption(self, text):
        text = text.lower()
        return ''.join(self._shift_char(x, -self.shift) for x in text)
    
    def _shift_char(self, char, shift):

        #Avoiding whitespace alteration
        if char == ' ':
            return ' '
        
        #Make sure char is a letter
        if char in self.letters:
            count = self.letters.index(char)
            shifted = (count + shift) % 26
            return self.letters[shifted]
        
        # Check if the character is a special character
        elif char in self.special:
            count = self.special.index(char)
            shifted = (count + shift) % len(self.special)
            return self.special[shifted]
        
        # For other characters (including punctuation), apply the shift
        else:
            return chr((ord(char) + shift) % 256)

# Example usage
cipher = CaesarCipher()
shift_there = cipher.encryption("Python lab rocks!!$%*)")
shift_back = cipher.decryption(shift_there)
print("With Encryption -- ", shift_there)
print("With Decryption -- ", shift_back)