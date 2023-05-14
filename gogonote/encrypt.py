import hashlib
import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, MultiFernet

class encrypting:
    #$$$  USER PASSWORD hashing and verifing #$$$
    def hashing(password):
        salt = b'vivekyadavdark'
        pwd = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,100000)
        return pwd

#$$$  ENCRYPT PASSWORD FOR SESSION VAR #$$$
    def get_encrypted_password(data):
        hashpaskey = hashlib.md5()
        hashpaskey.update(data.encode())
        return hashpaskey.hexdigest()

#$$$  ENCRYPT NOTES  #$$$
    def encrypt(data, key):
        key = key.encode('utf-8')
        salt = b'j\x1e\xb5\x97\x8f?L7c\xa8\xd9\x95\x0e\xdf%\x9a'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(key))
        f = Fernet(key)
        encrypted_mesg = f.encrypt(data.encode())
        print(' \nencrypted_mesg ',encrypted_mesg.decode('utf-8'),'\n')
        return encrypted_mesg.decode('utf-8')


#$$$  DECRYPT NOTES  #$$$
    def get_decrypted_not(data, key):
        key = key.encode()
        salt = b'j\x1e\xb5\x97\x8f?L7c\xa8\xd9\x95\x0e\xdf%\x9a'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(key))
        f = Fernet(key)

        for note in data:
            # nt = note['Notes']
            da = f.decrypt(note['note'].encode())
            da = da.decode('utf-8')
            note['note'] = da     

        return data

#$$ Valid secret_key  and give user old password
    def valid_secret_key(secret_key, email):
        with open('gogonote/keyfile.key', 'rb') as file:
            key = file.read()
        f = Fernet(key)
        secret_key = f.decrypt(secret_key.encode())
        secret_key = secret_key.decode('utf-8')
        
        print('\n',secret_key)
        if email in secret_key:
            secret_key = secret_key[4: -len(email)]
            print("Secret 2 :: ", secret_key, '\n')
        else:
            print('Invalid secret key ::\n',)
            return False
        
        #decrypt get password  change all notes format encrypt and cahnge password then
        passkey = f.decrypt(secret_key.encode())
        passkey = passkey.decode('utf-8')
        print('\npasskey :: ',passkey,"\n")
        print('\npasskey :: ',passkey,"\n")

        return passkey


#$$$ REENCRYPT NOTES -- when password is changed            1 =old    2=new
    def reecrypt_allnotes(all_notes, passkey1, passkey2):
        passkey1 = passkey1.encode()
        passkey2 = passkey2.encode()
        print("\npasskey1 :: ", passkey1, "\n")
        print("\npasskey2 :: ", passkey2)
        
        salt = b'j\x1e\xb5\x97\x8f?L7c\xa8\xd9\x95\x0e\xdf%\x9a'
        kdf = PBKDF2HMAC( algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        key1 = base64.urlsafe_b64encode(kdf.derive(passkey1))
        f1 = Fernet(key1)

        # salt = b'j\x1e\xb5\x97\x8f?L7c\xa8\xd9\x95\x0e\xdf%\x9a'
        kdf = PBKDF2HMAC( algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        key2 = base64.urlsafe_b64encode(kdf.derive(passkey2))
        f2 = Fernet(key2)

        ## ALL NOTES ARE ENCRYPT
        # 1. USE F1 TO DECRYPT NOTES FROM OLD KEY(PASS)
        # 2. USE F2 TO REENCRYPT NOTES FROM NEW KEY(PASSWORD)
        
        for note in all_notes:
            no = f1.decrypt(note['note'].encode())
            no = no.decode('utf-8')
            
            no = f2.encrypt(no.encode())
            no = no.decode('utf-8')
            note['note'] = no

        return all_notes







