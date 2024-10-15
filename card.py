from crypt_image import CryptImage
from PIL import Image

class Card:
    def __init__(self, name: str, creator: str, image: CryptImage, riddle: str, solution: str):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution
    def __repr__(self):
        return f"<Card name=\"{self.name}\", creator=\"{self.creator}\">"
    
    def __str__(self):
        if self.solution:
            return f"Card \"{self.name}\" by {self.creator}\n\triddle: \"{self.riddle}\"\n\tsolution: \"{self.solution}\""
        else:
            return f"Card \"{self.name}\" by {self.creator}\n\triddle: \"{self.riddle}\"\n\tsolution: unsolved"
        
    @classmethod
    def create_from_path(cls, name: str, creator: str, path: str, riddle: str, solution: str):
        return Card(name, creator, CryptImage.create_from_path(path), riddle, solution)
    
    def serialize(self) -> bytes:
        bytes_repr = b''
        name_encoded = self.name.encode('utf-8')
        creator_encoded = self.creator.encode()
        riddle_encoded = self.riddle.encode()

        bytes_repr = bytes_repr + len(name_encoded).to_bytes(4) + name_encoded
        bytes_repr = bytes_repr + len(creator_encoded).to_bytes(4) + creator_encoded
        bytes_repr = bytes_repr + self.image.image.size[0].to_bytes(4)
        bytes_repr = bytes_repr + self.image.image.size[1].to_bytes(4)
        bytes_repr = bytes_repr + self.image.image.tobytes()
        bytes_repr = bytes_repr + self.image.key_hash
        bytes_repr = bytes_repr + len(riddle_encoded).to_bytes(4) + riddle_encoded
        return bytes_repr

    @classmethod
    def deserialize(cls, data):
        name_size = int.from_bytes(data[:4])
        name = data[4:4+name_size].decode()
        creator_size = int.from_bytes(data[4+name_size:8+name_size])
        creator = data[8+name_size: 8+name_size+creator_size].decode()
        image_height = int.from_bytes(data[8+name_size+creator_size: 12+name_size+creator_size])
        image_width = int.from_bytes(data[12+name_size+creator_size: 16+name_size+creator_size])
        binary_image_data = data[16+name_size+creator_size: 16+name_size+creator_size+image_height*image_width*3]
        key_hash = data[16+name_size+creator_size+image_height*image_width*3: 48+name_size+creator_size+image_height*image_width*3]
        riddle_size = int.from_bytes(data[48+name_size+creator_size+image_height*image_width*3: 52+name_size+creator_size+image_height*image_width*3])
        riddle = data[52+name_size+creator_size+image_height*image_width*3: 52+name_size+creator_size+image_height*image_width*3+riddle_size].decode()
        #print(image_height*image_width*3)
        #print(len(binary_image_data))
        return Card(name, creator, CryptImage(Image.frombytes(mode="RGB", size=(image_height, image_width), data=binary_image_data), key_hash), riddle, None)
    
    def generate_identifier(self) -> str:
        return f"{self.creator}-{self.name}"
    
    def generate_creator_name_from_identifier(identifier) -> tuple[str,str]:
        return (identifier.split("-")[0],identifier.split("-")[1])