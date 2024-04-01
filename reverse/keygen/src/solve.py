AES_BLOCK_SIZE = 16

def decrypt_block(block, key):
    # Обратная операция к шифрованию блока: применение XOR
    decrypted_block = bytes([block[i] ^ (key[i] + i) for i in range(AES_BLOCK_SIZE)])
    return decrypted_block

def decrypt(ciphertext, key):
    num_blocks = len(ciphertext) // AES_BLOCK_SIZE
    decrypted_blocks = [decrypt_block(ciphertext[i * AES_BLOCK_SIZE: (i + 1) * AES_BLOCK_SIZE], key) for i in range(num_blocks)]
    decrypted_text = b''.join(decrypted_blocks)
    return decrypted_text

def main():
    key = b'issupersecretkey'
    
    # Введите зашифрованный текст в формате строки шестнадцатеричных чисел
    encrypted_hex = input("Введите зашифрованный текст (hex): ")
    ciphertext = bytes.fromhex(encrypted_hex)
    
    decrypted_text = decrypt(ciphertext, key)
    
    print("Decrypted:", decrypted_text.decode('utf-8'))

if __name__ == "__main__":
    main()
