import os
from dotenv import load_dotenv, set_key, find_dotenv
from key_generate import generate_rsa_key_pair, generate_aes_key

load_dotenv()


dotenv_path = find_dotenv()
rsa_pair = generate_rsa_key_pair()
aes_key = generate_aes_key()

KEYS = {
    "RSA_PRIVATE_KEY": rsa_pair[0],
    "RSA_PUBLIC_KEY": rsa_pair[1],
    "AES_KEY": aes_key,
}

def boot():
    for key,value in KEYS.items():
        if not os.getenv(key):
            set_key(dotenv_path, key, value.decode())
            print(f"{key} set to {value} in .env file")
        else:
            print(f"{key} already exists with value: {os.getenv(key)}")



if __name__ == "__main__":
    boot()


