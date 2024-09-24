import PIL
import hashlib
import Crypto
from PIL import Image
from Crypto.Cipher import AES
import io
import os


NONCE = b'arazim' 

class CryptImage():
    def __init__(self, image, key_hash):
        self.image = image
        self.key_hash = key_hash

    @classmethod
    def create_from_path(cls, path):
        crypt_img = CryptImage(Image.open(path),None)
        return crypt_img
    
    def encrypt(self, key: str) -> None:
        self.key_hash = hashlib.sha256(hashlib.sha256(key.encode()).digest()).digest()
        cipher = AES.new(hashlib.sha256(key.encode()).digest(), AES.MODE_EAX, nonce=NONCE)
        image_bytes_arr = self.image.tobytes()
        encrypted_image_bytes_arr = cipher.encrypt(image_bytes_arr)
        self.image = Image.frombytes('RGB', self.image.size,encrypted_image_bytes_arr,'raw')

    def decrypt(self, key: str) -> bool:
        if self.key_hash != hashlib.sha256(hashlib.sha256(key.encode()).digest()).digest():
            return False
        else:
            cipher = AES.new(hashlib.sha256(key.encode()).digest(), AES.MODE_EAX, nonce=NONCE)
            image_bytes_arr = self.image.tobytes()
            encrypted_image_bytes_arr = cipher.decrypt(image_bytes_arr)
            self.image = Image.frombytes('RGB', self.image.size,encrypted_image_bytes_arr,'raw')
            return True


if __name__ == "__main__":
    img = CryptImage.create_from_path("cat.jpg")
    img.encrypt("Arazim is the best")
    img.decrypt("Talpiot is the best")
    img.decrypt("Arazim is the best")