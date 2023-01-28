from abc import ABC, abstractmethod
from app.models.test.test import AddTest
import json

class RepositoryTest(ABC):
    @abstractmethod
    def get(self) -> AddTest:
        pass


class RepositoryAddTest(RepositoryTest):
    
    def get(self):
        with open('add_test.json', 'r', encoding='utf-8') as json_file:
            
           # data = json.load(json_file)

            add_test = json.loads(json_file.read())

            return add_test
