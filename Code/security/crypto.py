import cryptography
from cryptography.fernet import Fernet
import os

class CryptoHandler:
    """
    Handles Fernet encryption and decryption.
    """
    def __init__(self, key=None):
        """
        Initialize with a key or generate a new one.
        """
        if key:
            self.key = key
        else:
            self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

    @staticmethod
    def generate_key():
        """Generates a new Fernet key."""
        return Fernet.generate_key()

    def encrypt(self, data: str) -> str:
        """
        Encrypts a string and returns the encrypted data as a base64-encoded string.
        """
        if not isinstance(data, str):
            raise ValueError("Data to encrypt must be a string.")
        
        encrypted_bytes = self.fernet.encrypt(data.encode('utf-8'))
        return encrypted_bytes.decode('utf-8')

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypts a base64-encoded string and returns the original string.
        Raises cryptography.fernet.InvalidToken if decryption fails.
        """
        if not isinstance(encrypted_data, str):
            raise ValueError("Data to decrypt must be a string.")
            
        decrypted_bytes = self.fernet.decrypt(encrypted_data.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')

    def get_key(self) -> bytes:
        """Returns the current key."""
        return self.key