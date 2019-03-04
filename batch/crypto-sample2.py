import binascii
import binascii
from Crypto.Cipher import AES
from Crypto import Random

def get_random_byte_string(byte_length):
    return Random.get_random_bytes(byte_length)

def hex_string_to_byte_string(hex_string):
    return binascii.unhexlify(hex_string)

def make_keys(cipher_type, key_size, iv_size):
    """ Generate keys that are is dumpable to JSON
    """
    cipher_key = get_random_byte_string(key_size)    # 256 bits (32 bytes)
    cipher_iv  = get_random_byte_string(iv_size)    # 16 bytes (same as block size)
    
    return {
        "cipher":   cipher_type,
        "key":      binascii.hexlify(cipher_key).decode("utf-8"),
        "iv":       binascii.hexlify(cipher_iv).decode("utf-8")
    }

if __name__ == "__main__":
    print("START")
    aes_struct = make_keys("AES", 32, 16)
    # aes_key = get_random_byte_string(32)    # 256 bits (32 bytes)
    # aes_iv  = get_random_byte_string(16)    # 16 bytes (same as block size)
    print(aes_struct)

    # serialize aes_struct to file
    import json
    with open("cryptography-keys.json", "w+b") as f:
        f.write(json.dumps(aes_struct).encode("utf-8"))


    with open("cryptography-keys.json", "r+b") as f:
        aes_crypto_json = f.read()
    print(aes_crypto_json)
    aes_crypto2 = json.loads(aes_crypto_json)
    print(aes_crypto2)

    cipher_key = hex_string_to_byte_string(aes_crypto2['key'])
    cipher_iv  = hex_string_to_byte_string(aes_crypto2['iv'])
    print(cipher_key)
    print(cipher_iv)

    cipher = AES.new(cipher_key, AES.MODE_CFB, cipher_iv)
    cipher_text = cipher.encrypt("attack now".encode("utf-8"))
    hex_cipher_text = binascii.hexlify(cipher_text)
    print(hex_cipher_text)

    print("NOW TO DECRYPT")
    cipher = AES.new(cipher_key, AES.MODE_CFB, cipher_iv)
    cipher_text = binascii.unhexlify(hex_cipher_text)
    plain_text = cipher.decrypt(cipher_text).decode("utf-8")
    print("plain_text is {0}".format(plain_text))
    