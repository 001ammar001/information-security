from Crypto.Cipher import  PKCS1_OAEP
from Crypto.PublicKey import RSA

def encrypt(public_key, message ):    
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_message = cipher_rsa.encrypt(message)
    return enc_message



def decrypt(private_key,message):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    dec_message = cipher_rsa.decrypt(message)
    return dec_message

recipient_key = RSA.import_key(open("receiver.pem").read())
private_key = RSA.import_key(open("private.pem").read())

if __name__ == "__main__":
    print(recipient_key)
    print(encrypted := encrypt(recipient_key,b"abdullah"))
    print(decrypt(private_key,encrypted))