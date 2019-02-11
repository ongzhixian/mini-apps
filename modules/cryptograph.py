################################################################################
# Import statements
################################################################################

import logging

import binascii

from Crypto.Cipher import AES
from Crypto.Random import random

################################################################################
# Basic functions
################################################################################

########################################
# Define core functions
########################################

def get_random_byte_string(byte_length):
    """ Use this function to generate random byte string
    """
    byte_list = []
    i = 0
    while i < byte_length:
        byte_list.append(chr(random.getrandbits(8)))
        i = i + 1
    # Make into a string
    byte_string = ''.join(byte_list)
    return byte_string

def byte_string_to_hex_string(byte_string):
    return binascii.hexlify(byte_string)

def hex_string_to_byte_string(hex_string):
    return binascii.unhexlify(hex_string)

def make_keys(cipher_type, key_size, iv_size):
    """ Generate keys that are is dumpable to JSON
    """
    cipher_key = get_random_byte_string(key_size)    # 256 bits (32 bytes)
    cipher_iv  = get_random_byte_string(iv_size)    # 16 bytes (same as block size)
    
    return {
        "cipher":   cipher_type,
        "key":      binascii.hexlify(cipher_key),
        "iv":       binascii.hexlify(cipher_iv)
    }
    # import json
    # with open("cryptography-keys.json", "w+b") as f:
    #     f.write(json.dumps(cryptography))


########################################
# AES Encrypt/Decrypt functions
########################################

def aes_encrypt(cipher_key, cipher_iv, plain_text):
    cipher = AES.new(cipher_key, AES.MODE_CFB, cipher_iv)
    cipher_text = cipher.encrypt(plain_text)
    return cipher_text

def aes_decrypt(cipher_key, cipher_iv, cipher_text):
    cipher = AES.new(cipher_key, AES.MODE_CFB, cipher_iv)
    plain_text = cipher.decrypt(cipher_text)
    return plain_text

def aes_sample_usage():
    aes_key = get_random_byte_string(32)    # 256 bits (32 bytes)
    aes_iv  = get_random_byte_string(16)    # 16 bytes (same as block size)

    # Hardcode for re-testability
    aes_key_hex_string = "480b41eec90e92aabe6ec159768d7d88fa64eb35a91c7e5c39b89be53eab0d06"
    aes_iv_hex_string = "ed0306cc63b48a3ab0405608aa4ea334"

    aes_key = hex_string_to_byte_string(aes_key_hex_string)
    aes_iv  = hex_string_to_byte_string(aes_iv_hex_string)

    cipher_text = aes_encrypt(aes_key, aes_iv, "Attack at dawn")
    print(cipher_text)

    plain_text = aes_decrypt(aes_key, aes_iv, cipher_text)
    print(plain_text)


# TODO: Implement KDF
# https://www.dlitz.net/software/pycrypto/api/current/Crypto.Protocol.KDF-module.html

################################################################################
# Variables dependent on Application basic functions
################################################################################

# N/A

################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    pass