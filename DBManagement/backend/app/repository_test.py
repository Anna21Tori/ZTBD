from abc import ABC, abstractmethod
from app.models.test.test import AddTest, ResultTest, ResultFiltersTest
import json
from dataclasses import dataclass
import typing as t



class RepositoryTest(ABC):
    @abstractmethod
    def get(self) -> AddTest:
        pass


class RepositoryAddTest(RepositoryTest):
    
    def get(self):

        result: ResultTest = ResultTest(mongodb=[], postgresql=[], redis=[])


        with open(f'add_test_mongodb.json', 'r', encoding='utf-8') as json_file:

            result.mongodb = AddTest(**json.loads(json_file.read()))

        with open(f'add_test_postgresql.json', 'r', encoding='utf-8') as json_file:
            result.postgresql = AddTest(**json.loads(json_file.read()))

        with open(f'add_test_redis.json', 'r', encoding='utf-8') as json_file:

            result.redis = AddTest(**json.loads(json_file.read()))

        return result

class RepositoryDelTest(RepositoryTest):
    
    def get(self):

        result: ResultTest = ResultTest(mongodb=[], postgresql=[], redis=[])


        with open(f'del_test_mongodb.json', 'r', encoding='utf-8') as json_file:

            result.mongodb = AddTest(**json.loads(json_file.read()))

        with open(f'del_test_postgresql.json', 'r', encoding='utf-8') as json_file:

            result.postgresql = AddTest(**json.loads(json_file.read()))

        return result

class RepositoryFiltersTest(RepositoryTest):
    
    def get(self):
        sqls = ["FROM books WHERE books.pages > 100 AND books.pages < 300",
        "SELECT * FROM categories JOIN books ON categories.book_id = books.id JOIN quotes ON quotes.book_id = books.id WHERE books.lang = 'polski' AND books.pages > 100 AND books.pages < 200 AND quotes.content LIKE 'to'"]
        result: ResultFiltersTest = ResultFiltersTest(mongodb=[], postgresql=[], redis=[], sqls=sqls)


        with open(f'filter_test_mongodb.json', 'r', encoding='utf-8') as json_file:

            result.mongodb = AddTest(**json.loads(json_file.read()))

        with open(f'filter_test_postgresql.json', 'r', encoding='utf-8') as json_file:

            result.postgresql = AddTest(**json.loads(json_file.read()))
        
        with open(f'filter_test_postgresql.json', 'r', encoding='utf-8') as json_file:

            result.redis = AddTest(**json.loads(json_file.read()))

        return result