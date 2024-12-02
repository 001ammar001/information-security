from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from key_generate import generate_aes_key
from Crypto.Random import get_random_bytes


def encrypt(key ,message = "", iv = b"0123456789abcdef"):    
    cipher = AES.new(key, AES.MODE_CBC,iv=iv)
    enc_message = cipher.encrypt(pad(message, AES.block_size))
    return enc_message



def decrypt(key, message = "", iv = b"0123456789abcdef"):
    cipher = AES.new(key, AES.MODE_CBC,iv=iv)
    dec_message = cipher.decrypt(message)
    return unpad(dec_message,AES.block_size)


message = b"abdul rahman" 

if __name__ == "__main__":
    key = generate_aes_key()
    print(message := encrypt(key,message))
    print(decrypt(key,message).decode())