from Crypto.PublicKey import RSA

def generate_key_pair():
    key = RSA.generate(1024)
    private_key = key.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)
    file_out.close()
    public_key = key.publickey().export_key()
    file_out = open("receiver.pem", "wb")
    file_out.write(public_key)
    file_out.close()



if __name__ == "__main__":
    generate_key_pair()