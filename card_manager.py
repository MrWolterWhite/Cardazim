from card import Card
import os
import json
from file_system_driver import FileSystemDriver
from sql_driver import SqlDriver
from PIL import Image

class CardManager:

    def __init__(self, database_url: str, images_url: str):
        self.driver = self.get_driver(database_url, images_url)
        self.images_url = images_url

    def get_driver(self, database_url: str, images_url: str):
        #important!!!! check that the OS gets the url with "filesystem" suffix
        driver_option = database_url.split(":")[0]
        if driver_option == "filesystem":
            return FileSystemDriver(database_url.split(":")[1][2:], images_url)
        elif driver_option == "sql":
            return SqlDriver(database_url.split(":")[1][2:], images_url)
        else:
            return None


    def save(self, card: Card, dir_path: str):
        self.driver.dir = dir_path
        self.driver.save(card, card.generate_identifier())

    def get_identifier(self, card: Card) -> str:
        return card.generate_identifier()
    
    def load(self, identifier: str) -> Card:
        return self.driver.load(identifier)
    
    def get_creators(self) -> [str]:
        return self.driver.getCreators()
    
    def get_creator_cards(self, creator: str) -> [Card]:
        return self.driver.getCreatorCards(creator)
    
