def xor_encrypt(text, key):
    encrypted_text = ""
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return encrypted_text


def xor_decrypt(text, key):
    decrypted_text = ""
    for i in range(len(text)):
        decrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return decrypted_text


# Пример использования
text = "krdu{l33t_4rdu1n0_1s_4m4z1ng}"
key = "\x13\x37\x20\x24"  # пример ключа

encrypted_text = xor_encrypt(text, key)
print("Зашифрованный текст:", encrypted_text.encode("ascii"))

decrypted_text = xor_decrypt(encrypted_text, key)
print("Дешифрованный текст:", decrypted_text)
