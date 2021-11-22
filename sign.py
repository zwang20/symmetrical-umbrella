"""
sign.py

signs a public key
"""

import json
import os
import time

import rsa

with open("key.pub", "r", encoding="utf-8") as file:
    public_key = file.read()

user_id = int(input("Enter user id: "), 16)

# get unix timestamp
timestamp = int(time.time())

cert = {
    "public_key": public_key,
    "user_id": user_id,
    "timestamp": timestamp,
}

# save cert
with open(f'{user_id}.json', 'w', encoding="utf-8") as cert_file:
    json.dump(cert, cert_file, indent=4)

# load private key
with open(os.path.join('data', 'keys', 'key'), 'rb') as private_key_file:
    private_key = rsa.PrivateKey.load_pkcs1(private_key_file.read())

# load public key
with open(os.path.join('data', 'keys', 'key.pub'), 'rb') as public_key_file:
    public_key = rsa.PublicKey.load_pkcs1(public_key_file.read())

# read certificate
with open(f'{user_id}.json', 'r', encoding="utf-8") as cert_file:
    certificate = cert_file.read().encode('utf-8')

# sign certificate
signature = rsa.sign(certificate, private_key, 'SHA-512')

# verify sign
rsa.verify(certificate, signature, public_key)

# save sign
with open(f'{user_id}.pem', 'wb') as sign_file:
    sign_file.write(signature)
