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
        
    def replace(self, prev_card: Card, new_card: Card):
        image_path = os.path.join(self.image_url,new_card.generate_identifier())
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        image_path = os.path.join(image_path, "image.png")
        new_card.image.image.save(image_path,"png")
        prompt1 = f"""DELETE FROM Cards WHERE name=\'{prev_card.name}\' AND creator=\'{prev_card.creator}\' AND riddle=\'{prev_card.riddle}\';"""
        self.cur.execute(prompt1)
        self.con.commit()
        prompt2 = """INSERT INTO Cards(name, creator, riddle, solution, image_path, key_hash) VALUES (?,?,?,?,?,?);"""
        self.cur.execute(prompt2, (new_card.name, new_card.creator, new_card.riddle, new_card.solution, image_path, new_card.image.key_hash))
        self.con.commit()

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
            
    def GetCreators(self) -> list[str]:
        res = self.cur.execute("SELECT creator FROM Cards")
        creators = res.fetchall()
        creators = [val for (val,) in creators]
        return list(set(creators))
    
    def GetCreatorCards(self, creator: str) -> list[Card]:
        res = self.cur.execute(f"SELECT * FROM Cards WHERE creator=\'{creator}\'")
        cards_data = res.fetchall()
        cards = [Card(name, creator, CryptImage(Image.open(image_path), key_hash), riddle, solution) for (name, creator, riddle, solution, image_path, key_hash) in cards_data]
        return cards
    
    def GetCreatorCard(self, creator: str, card_name: str) -> Card:
        res = self.cur.execute(f"SELECT * FROM Cards WHERE creator=\'{creator}\' AND name=\'{card_name}\'")
        cards_data = res.fetchall()
        cards = [Card(name, creator, CryptImage(Image.open(image_path), key_hash), riddle, solution) for (name, creator, riddle, solution, image_path, key_hash) in cards_data]
        return cards[0]
    
    def GetCreatorSolvedCards(self, creator: str) -> list[Card]:
        res = self.cur.execute(f"SELECT * FROM Cards WHERE creator=\'{creator}\' AND solution IS NOT NULL")
        cards_data = res.fetchall()
        cards = [Card(name, creator, CryptImage(Image.open(image_path), key_hash), riddle, solution) for (name, creator, riddle, solution, image_path, key_hash) in cards_data]
        return cards
    
    def GetCreatorUnsolvedCards(self, creator: str) -> list[Card]:
        res = self.cur.execute(f"SELECT * FROM Cards WHERE creator=\'{creator}\' AND solution IS NULL")
        cards_data = res.fetchall()
        cards = [Card(name, creator, CryptImage(Image.open(image_path), key_hash), riddle, solution) for (name, creator, riddle, solution, image_path, key_hash) in cards_data]
        return cards
    
    def GetFilteredCards(self, creator: str, name: str, riddle: str, solution: str):
        res = self.cur.execute(f"SELECT * FROM Cards WHERE (creator=\'{creator}\' OR {creator==''}) AND (name=\'{name}\' OR {name==''}) AND (riddle=\'{riddle}\' OR {riddle==''}) AND (solution=\'{solution}\' OR {solution==''})")
        cards_data = res.fetchall()
        cards = [Card(name, creator, CryptImage(Image.open(image_path), key_hash), riddle, solution) for (name, creator, riddle, solution, image_path, key_hash) in cards_data]
        return cards




