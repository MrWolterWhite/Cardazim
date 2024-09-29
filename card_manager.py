from card import Card
import os
import json
from PIL import Image

class CardManager:
    def save(self, card: Card, dir_path: str):
        print(self.get_identifier(card))
        self_path = os.path.join(dir_path, self.get_identifier(card))
        os.makedirs(self_path)
        image_path = os.path.join(self_path, "image.png")
        json_data = json.dumps([card.name, card.creator, card.riddle, card.solution, image_path])
        json_path = os.path.join(self_path, "metadata.json")
        with open(json_path,"w") as json_file:
            json_file.write(json_data)
        card.image.image.save(image_path,"png")
    def get_identifier(self, card: Card) -> str:
        return card.generate_identifier()
    def load(self, identifier: str) -> Card:
        pass
    
