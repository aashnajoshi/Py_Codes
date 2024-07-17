text = 'Hello World!'
custom_key = 'python'
offset = len(custom_key)
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def caesar(message, offset): #Caesar cipher, every single letter is always encrypted with the same letter, depending on the specified offset
    final_message = ''  
    for char in message:
        if not char.isalpha(): # Append any non-letter character to the message
            final_message += char
        else:
            char_lower = char.lower()
            index = alphabet.index(char_lower)
            new_index = (index + offset) % 26
            if char.isupper():
                final_message += alphabet[new_index].upper()
            else:
                final_message += alphabet[new_index]
    return final_message

def vigenere(message, key, direction=1): #Vigenère cipher, where offset for each letter is determined by unique key
    final_message = ''
    key_index = 0
    for char in message.lower():
        if not char.isalpha(): # Append any non-letter character to the message
            final_message += char
        else:        
            key_char = key[key_index % len(key)]
            key_index += 1
            offset = alphabet.index(key_char)
            index = alphabet.find(char)
            new_index = (index + offset*direction) % len(alphabet)
            final_message += alphabet[new_index]
    return final_message

def encrypt(message, key):
    return vigenere(message, key)
    # return caesar(message,offset)
    
def decrypt(message, key):
    return vigenere(message, key, -1)
    # return caesar(message, -offset)
    
print(f'Original text: {text}')
print(f'Key: {custom_key}\n')

encryption = encrypt(text, custom_key)
print(f'Encrypted text: {encryption}')
decryption = decrypt(encryption, custom_key)
print(f'Decrypted text: {decryption}')