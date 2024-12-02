from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import random
import string
def generate_rsa_key_pair():
    key = RSA.generate(1024)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return (private_key,public_key)

def generate_aes_key():
    key = "".join(random.choices(string.ascii_letters + string.digits,k=16))
    return key.encode()

