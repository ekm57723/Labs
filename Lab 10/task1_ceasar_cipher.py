class Caesar:
    def __init__(self, key=0):
        
        self._key = key

    def get_key(self):
        
        return self._key

    def set_key(self, key):
       
        self._key = key

    def encrypt(self, plaintext):
        
        return ''.join(_shift_char(c.lower(), self._key) for c in plaintext)

    def decrypt(self, ciphertext):
        
        return ''.join(_shift_char(c.lower(), -self._key) for c in ciphertext)


def _shift_char(char, key):
    
    if char.isalpha():
        base = ord('a')
        return chr((ord(char) - base + key) % 26 + base)
    elif char == ' ':
        return char
    else:
        return chr((ord(char) + key) % 128) 

#Testing
if __name__ == "__main__":
    
    cipher = Caesar()
    cipher.set_key(3)
    print(cipher.encrypt("hello WORLD!"))  
    print(cipher.decrypt("KHOOR zruog$"))  

    cipher.set_key(6)
    print(cipher.encrypt("zzz")) 
    print(cipher.decrypt("FFF")) 

    cipher.set_key(-6)
    print(cipher.encrypt("FFF")) 