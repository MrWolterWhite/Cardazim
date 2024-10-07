import PIL.Image
from card_driver import CardDriver
import os
import json
import PIL
import functools
from crypt_image import CryptImage
from card import Card
class FileSystemDriver(CardDriver):
    def __init__(self, dir, image_url):
        self.dir = dir
        self.image_url = image_url
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def save(self, card: Card, id):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        self_path = os.path.join(self.dir, id)
        image_path = os.path.join(self.image_url,id)
        if not os.path.exists(self_path):
            os.makedirs(self_path)
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        image_path = os.path.join(image_path, "image.png")
        json_data = json.dumps([card.name, card.creator, card.riddle, card.solution, image_path, str(card.image.key_hash)])
        json_path = os.path.join(self_path, "metadata.json")
        with open(json_path,"w") as json_file:
            json_file.write(json_data)
        card.image.image.save(image_path,"png")

    def load(self, id) -> Card:
        self_path = os.path.join(self.dir, id)
        json_path = os.path.join(self_path, "metadata.json")
        json_data = None
        with open(json_path,"r") as json_file:
            json_data = json.loads(json_file.read())
        image = PIL.Image.open(json_data[4])
        return Card(json_data[0],json_data[1],CryptImage(image, bytes(json_data[5])),json_data[2],json_data[3])
    
    def getCreators(self):
        dir_list = os.listdir(self.dir)
        creators_list = {''}
        for curr_dir in dir_list:
            if os.path.isdir(curr_dir):
                self_path = os.path.join(self.dir, curr_dir)
                json_path = os.path.join(self_path, "metadata.json")
                json_data = None
                if os.path.isfile(json_path):
                    with open(json_path,"r") as json_file:
                        json_data = json.loads(json_file.read())
                    creators_list.add(json_data[1])
        return filter(lambda x: x!='', list(creators_list))
    
    def getCreatorCards(self, creator: str):
        dir_list = os.listdir(self.dir)
        card_list = []
        for curr_dir in dir_list:
            if os.path.isdir(curr_dir):
                self_path = os.path.join(self.dir, curr_dir)
                json_path = os.path.join(self_path, "metadata.json")
                json_data = None
                if os.path.exists(json_path) and os.path.isfile(json_path):
                    with open(json_path,"r") as json_file:
                        json_data = json.loads(json_file.read())
                    curr_creator = json_data[1]
                    if curr_creator == creator :
                        image = PIL.Image.open(json_data[4])
                        curr_card = Card(json_data[0],json_data[1],CryptImage(image, bytes(json_data[5])),json_data[2],json_data[3])
                        card_list.append(curr_card)        
        return card_list


