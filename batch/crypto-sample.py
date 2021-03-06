import binascii
from Crypto.Random import random


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


# def aes_encrypt():
#     key = b'Sixteen byte key'
#     iv = Random.new().read(AES.block_size)
#     cipher = AES.new(key, AES.MODE_CFB, iv)
#     msg = iv + cipher.encrypt(b'Attack at dawn')

def aes_encrypt(cipher_key, cipher_iv, plain_text):
    cipher = AES.new(cipher_key, AES.MODE_CFB, cipher_iv)
    cipher_text = cipher.encrypt(plain_text)
    return cipher_text

def aes_decrypt(cipher_key, cipher_iv, cipher_text):
    cipher = AES.new(cipher_key, AES.MODE_CFB, cipher_iv)
    plain_text = cipher.decrypt(cipher_text)
    return plain_text



from Crypto.Cipher import AES

if __name__ == "__main__":
    print("OK")
    
    # aes_key = random.getrandbits(256)   # 256 bits
    # aes_iv  = random.getrandbits(16)    # 16 bits (same as block size)
    aes_key = get_random_byte_string(32)    # 256 bits (32 bytes)
    aes_iv  = get_random_byte_string(16)    # 16 bytes (same as block size)

    import pdb
    pdb.set_trace()

    aes_key_hex_string = "480b41eec90e92aabe6ec159768d7d88fa64eb35a91c7e5c39b89be53eab0d06"
    aes_iv_hex_string = "ed0306cc63b48a3ab0405608aa4ea334"

    aes_key = hex_string_to_byte_string(aes_key_hex_string)
    aes_iv  = hex_string_to_byte_string(aes_iv_hex_string)

    cipher_text = aes_encrypt(aes_key, aes_iv, "Attack at dawn")
    print(cipher_text)

    plain_text = aes_decrypt(aes_key, aes_iv, cipher_text)
    print(plain_text)

    cryptography = {
        "cipher": "AES",
        "key": aes_key_hex_string,
        "iv": aes_iv_hex_string,
    }
    import json
    with open("cryptography-keys.json", "w+b") as f:
        f.write(json.dumps(cryptography))


    # cipher = AES.new(aes_key, AES.MODE_CFB, aes_iv)
    # msg = cipher.encrypt(b'Attack at dawn')
    
    # print("aes_key: {0}".format(binascii.hexlify(aes_key)))
    # print("aes_iv:  {0}".format(binascii.hexlify(aes_iv)))
    # x = binascii.hexlify(aes_iv)
    # print("Xsg:     {0}".format(type(x)))
    # print("msg:     {0}".format(msg))

    # hex_enc = binascii.hexlify(msg)

    # #x = cipher.decrypt(msg)
    # print(hex_enc)

    # cipher = AES.new(aes_key, AES.MODE_CFB, aes_iv)
    # plain_text = cipher.decrypt(msg)
    # print(plain_text)

    # # a = get_random_byte_string(32)
    # # b = random.getrandbits(8 * 32)
    # # print(a, len(a))
    # # print(b)
    # # print(binascii.hexlify(a))
    # # print(hex(a))