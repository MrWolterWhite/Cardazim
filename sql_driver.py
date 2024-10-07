from card_driver import CardDriver
from card import Card
from crypt_image import CryptImage
import os
import sqlite3
from PIL import Image

class SqlDriver(CardDriver):
    def __init__(self, dir, image_url):
        self.con = sqlite3.connect(f"{dir}.db")
        self.cur = self.con.cursor()
        self.dir = dir
        self.image_url = image_url
        self.cur.execute("CREATE TABLE IF NOT EXISTS Cards(name, creator, riddle, solution, image_path, key_hash)")
        
    
    def save(self, card: Card, id):
        image_path = os.path.join(self.image_url,id)
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        image_path = os.path.join(image_path, "image.png")
        card.image.image.save(image_path,"png")
        prompt = """INSERT INTO Cards(name, creator, riddle, solution, image_path, key_hash) VALUES (?,?,?,?,?,?);"""
        self.cur.execute(prompt, (card.name, card.creator, card.riddle, card.solution, image_path, card.image.key_hash))
        self.con.commit()
        

    def load(self, id) -> Card:
        res = self.cur.execute("SELECT * FROM Cards")
        cards_data = res.fetchall()
        cards = [Card(name, creator, CryptImage(None, key_hash), riddle, solution) for (name, creator, riddle, solution, _, key_hash) in cards_data]
        for card in cards:
            if card.generate_identifier() == id:
                card_singleton = [card_data for card_data in cards_data if card_data[0] == card.name and card_data[1] == card.creator and card_data[2] == card.riddle and card_data[3] == card.solution and card_data[5] == card.image.key_hash]
                card.image.image =  Image.open(f"{card_singleton[0][4]}")
                return card
            
    def GetCreators(self) -> [str]:
        res = self.cur.execute("SELECT creator FROM Cards")
        creators = res.fetchall
        creators = [val for (val,) in creators]
        return list(set(creators))
    
    def GetCreatorCards(self, creator: str) -> [Card]:
        res = self.cur.execute(f"SELECT * FROM Cards WHERE creator=\'{creator}\'")
        cards_data = res.fetchall()
        cards = [Card(name, creator, CryptImage(Image.open(image_path), key_hash), riddle, solution) for (name, creator, riddle, solution, image_path, key_hash) in cards_data]
        return cards



