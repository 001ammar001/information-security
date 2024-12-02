from symmetric_crypt import encrypt
from dotenv import load_dotenv
import os


load_dotenv()

print(key := os.environ.get("AES_KEY"))
print(encrypt(key=key.encode(),message=b"message"))