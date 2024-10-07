from abc import ABC, abstractmethod
from card import Card
class CardDriver(ABC):
    @abstractmethod
    def save(self, card: Card, id):
        ...
    def load(self, id) -> Card:
        ...
    def GetCreators(self):
        ...
    def GetCreatorCards(self, creator: str):
        ...
    
    
