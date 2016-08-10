def cipher(string):
    return ''.join(chr(219-ord(c)) if 'a'<=c<='z' else c for c in string)

if __name__=="__main__":
    sentence="Hello, world!"
    ciphertext=cipher(sentence)
    print(sentence)
    print(ciphertext)
    print(cipher(ciphertext)) 