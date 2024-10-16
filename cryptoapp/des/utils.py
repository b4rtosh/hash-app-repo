import os

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import itertools

def des_encrypt(plaintext, key):
    """
    Encrypts plaintext using DES.
    :param plaintext: The message to encrypt.
    :param key: The key (must be 8 bytes for DES).
    :return: Ciphertext and IV.
    """
    cipher = DES.new(key, DES.MODE_CBC)
    iv = cipher.iv  # Initialization vector
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), DES.block_size))
    return ciphertext, iv


def des_decrypt(ciphertext, key, iv):
    """
    Decrypts ciphertext using DES.
    :param ciphertext: The encrypted message.
    :param key: The key used for encryption.
    :param iv: The initialization vector used for encryption.
    :return: Decrypted message.
    """
    try:
        cipher = DES.new(key, DES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(ciphertext), DES.block_size)
        return decrypted_data
    except (ValueError, KeyError):
        pass  # Ignore decryption errors and move to the next key


def des_brute_force(ciphertext, iv):
    """
    Attempts to brute force the DES key.
    :param ciphertext: The encrypted message (ciphertext).
    :param iv: The initialization vector used for encryption.
    :return: Decrypted message if the key is found, otherwise None.
    """
    charset = 'abcdefghijklmnopqrstuvwxyz'  # Limiting to lowercase letters
    key_length = 8  # DES keys are always 8 bytes

    for key_tuple in itertools.product(charset, repeat=key_length):
        key = ''.join(key_tuple).encode('utf-8')
        try:
            cipher = DES.new(key, DES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(ciphertext), DES.block_size)
            print(f"Success! Key: {key}, Decrypted message: {decrypted_data}")
            return decrypted_data, key
        except (ValueError, KeyError):
            pass  # Ignore decryption errors and move to the next key

    print("Key not found.")
    return None, None


def des_dictionary_attack(ciphertext, iv, dictionary_file):
    """
    Perform a dictionary attack on DES using an uploaded dictionary file.
    :param ciphertext: Encrypted ciphertext to be cracked.
    :param iv: Initialization vector used for decryption.
    :param dictionary_file: File object containing dictionary words (uploaded).
    :return: Tuple of (decrypted message, key) if successful, else None.
    """
    # Read the uploaded dictionary file line by line
    for word in dictionary_file:
        # Decode and strip newlines or extra spaces, ensure it's 8 bytes long
        key = word.strip().ljust(8, b'\0')[:8]
        decrypted_data = des_decrypt(ciphertext, key, iv)
        if decrypted_data:  # If decryption is successful
            return decrypted_data, key  # Return the decrypted message and key

    return None, None  # Return None if no key worked