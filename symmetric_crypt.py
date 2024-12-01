from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt(key ,message ):    
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    enc_message = cipher.encrypt(pad(message, AES.block_size))
    return enc_message



def decrypt(key,message,iv):
    cipher = AES.new(key, AES.MODE_CBC,iv=iv)
    dec_message = cipher.decrypt(message)
    return dec_message