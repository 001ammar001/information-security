from Crypto.Cipher import  PKCS1_OAEP
from Crypto.PublicKey import RSA
from key_generate import generate_rsa_key_pair

def encrypt(public_key, message ):    
    public_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_message = cipher_rsa.encrypt(message)
    return enc_message



def decrypt(private_key,message):
    private_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    dec_message = cipher_rsa.decrypt(message)
    return dec_message

private_key,recipient_key = generate_rsa_key_pair() 

if __name__ == "__main__":
    print(recipient_key)
    print(encrypted := encrypt(recipient_key,b"abduldlkjslkjdlklah hi there hi there hi there"))
    print(decrypt(private_key,encrypted))

