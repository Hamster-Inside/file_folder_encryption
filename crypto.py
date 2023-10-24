import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from abc import ABC, abstractmethod


class Crypto(ABC):

    def __init__(self, path):
        self.path = path

    @staticmethod
    def create_key(password):
        salt = b'\x9f\xe7\xba\xa6\xe6\x14\xf3\x9c\xe1\xaf\x12\t\xfc\x00\xbc\x92\xc3\t\xda\x8c\xd1\x02'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        return key

    @abstractmethod
    def execute(self):
        pass


class Decryption(Crypto):

    def execute(self, password):
        try:
            with open(self.path, 'r') as file:
                data_to_decrypt = file.read()
        except FileNotFoundError:
            print(f'File not found: {self.path}')
            return False

        fernet = Fernet(self.create_key(password))

        decrypted_content = fernet.decrypt(data_to_decrypt.encode('utf-8'))

        with open(self.path.rename(self.path.with_suffix('')), 'w') as file:
            file.write(decrypted_content.decode('utf-8'))
        return True


class Encryption(Crypto):

    def execute(self, password):
        try:
            with open(self.path, 'r') as file:
                data_to_encrypt = file.read()
        except FileNotFoundError:
            print(f'File not found: {self.path}')
            return False
        fernet = Fernet(self.create_key(password))
        encrypted_content = fernet.encrypt(data_to_encrypt.encode('utf-8'))

        with open(self.path.rename(self.path.with_suffix(self.path.suffix + '.encrypted')), 'w') as file:
            file.write(encrypted_content.decode('utf-8'))
        return True


class Append(Crypto):

    def __init__(self, path, text):
        super().__init__(path)
        self.text = text.encode('utf-8')

    def execute(self, password):
        with open(self.path, 'r') as file:
            data = file.read()

        fernet = Fernet(self.create_key(password))
        encrypted_content = fernet.decrypt(data.encode('utf-8'))

        encrypted_content += "\n"
        encrypted_content += self.text

        encrypted_content = fernet.encrypt(encrypted_content)

        with open(self.path, 'w') as file:
            file.write(encrypted_content.decode('utf-8'))
