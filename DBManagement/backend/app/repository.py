from abc import ABC, abstractmethod
from app.models.book.book import BookDB, BookMongo, BookCreate, Book as BookModel
from app.models.comment.comment import CommentDB, CommentMongo, CommentCreate, Comment
from app.models.quote.quote import QuoteDB, QuoteMongo, QuoteCreate
from app.models.category.category import CategoryDB, CategoryMongo, CategoryCreate, Category
from app.databases.sql import SessionLocal, Base, engine
from app.databases.mongo import db as mongodb
import typing as t
from dataclasses import dataclass
import time

@dataclass
class Book:
    book: BookCreate
    comments: t.List[CommentCreate]
    quotes: t.List[QuoteCreate]
    categories: t.List[CategoryCreate]


class RepositoryDAO(ABC):
    @abstractmethod
    def save(self, books: t.List[Book]):
        pass
    @abstractmethod
    def save_all(self, books: t.List[Book]):
        pass
    @abstractmethod
    def delete(self, count: int):
        pass
    @abstractmethod
    def clear_db(self):
        pass
    @abstractmethod
    def filter_test_1(self):
        pass
    @abstractmethod
    def filter_test_2(self):
        pass
    # @abstractmethod
    # def filter_test_3(self):
    #     pass

class RepositorySql(RepositoryDAO):

    def __init__(self) -> None:
        super().__init__()
        self.session = SessionLocal()

    def save(self, books: t.List[Book]):
        _books: t.List[BookDB] = []

        for book in books:
            _book = BookDB(**book.book.dict())
            _books.append(_book)

        start_time = time.time()
        self.session.add_all(_books)
        self.session.commit()
        end_time = time.time()

        return (end_time-start_time)*1000

    def save_all(self, books: t.List[Book]):
        _books: t.List[BookDB] = []
        _categories: t.List[CategoryDB] = []
        _comments: t.List[CommentDB] = []
        _quotes: t.List[QuoteDB] = []
    
        for book in books:

            _book = BookDB(**book.book.dict())
            _books.append(_book)

            for category in book.categories:
                _category = CategoryDB(**category.dict())
                _categories.append(_category)

            for comment in book.comments:
                _comment = CommentDB(**comment.dict())
                _comments.append(_comment)

            for quote in book.quotes:
                _quote = QuoteDB(**quote.dict())
                _quotes.append(_quote)

        start_time = time.time()
        self.session.add_all(_books)
        self.session.add_all(_categories)
        self.session.add_all(_comments)
        self.session.add_all(_quotes)
        self.session.commit()
        end_time = time.time()

        return (end_time-start_time)*1000

    def delete(self, count: int):

        _books = self.session.query(BookDB).filter(BookDB.id < count)
        _comments = self.session.query(CommentDB).filter(CommentDB.book_id < count)
        _categories = self.session.query(CategoryDB).filter(CategoryDB.book_id < count)
        _quotes = self.session.query(QuoteDB).filter(QuoteDB.book_id < count)

        start_time = time.time()
        for book in _books:
            self.session.delete(book)
        for comment in _comments:
            self.session.delete(comment)
        for category in _categories:
            self.session.delete(category)
        for quote in _quotes:
            self.session.delete(quote)
        self.session.commit()
        end_time = time.time()

        return (end_time-start_time)*1000

    def filter_test_1(self):
        start_time = time.time()
        query = self.session.query(BookDB).filter(BookDB.pages > 100, BookDB.pages < 200)
        end_time = time.time()
        # print(str(query))
        return [query.count(), (end_time-start_time)*1000, "FROM books WHERE books.pages > 100 AND books.pages < 300"]

    def filter_test_2(self):
        categories = ["dramat", "komedia", "tragedia", "horror", "fantasy", "historia", "romans"]
        language = "polski"
        start_time = time.time()
        subquery_categories = self.session.query(CategoryDB.book_id).filter(CategoryDB.name.in_(categories))
        subquery_quotes = self.session.query(QuoteDB.book_id).filter(QuoteDB.content.contains('to'))
        query = self.session.query(BookDB)\
            .filter(BookDB.id.in_(subquery_categories))\
            .filter(BookDB.lang == language)\
            .filter(BookDB.pages > 100, BookDB.pages < 200)\
            .filter(BookDB.id.in_(subquery_quotes))
        end_time = time.time()
        # print(str(query))
        return [query.count(), (end_time-start_time)*1000, "SELECT * FROM categories JOIN books ON categories.book_id = books.id JOIN quotes ON quotes.book_id = books.id WHERE books.lang = 'polski' AND books.pages > 100 AND books.pages < 200 AND quotes.content LIKE 'to'"]

    def clear_db(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

class RepositoryMongo(RepositoryDAO):

    def __init__(self) -> None:
        super().__init__()
        self.db = mongodb


    def save_all(self, books: t.List[Book]):
        _books: t.List[any] = []

        for book in books:

            comments: t.List[CommentMongo] = []
            for comment in book.comments:
                comment_mongo = CommentMongo(**comment.dict())
                comments.append(comment_mongo)

            categories: t.List[CategoryMongo] = []
            for category in book.categories:
                category_mongo = CategoryMongo(**category.dict())
                categories.append(category_mongo)

            quotes: t.List[QuoteMongo] = []
            for quote in book.quotes:
                quote_mongo = QuoteMongo(**quote.dict())
                quotes.append(quote_mongo)

            book_mongo = BookMongo(**book.book.dict())
            book_mongo.comments = comments
            book_mongo.categories = categories
            book_mongo.quotes = quotes
            book_json = book_mongo.dict(by_alias=True)

            _books.append(book_json)

        start_time = time.time()
        self.collection = self.db.get_collection("books")
        self.collection.insert_many(_books)
        end_time = time.time()

        return (end_time-start_time)*1000

    def save(self, books: t.List[Book]):
        _books: t.List[any] = []

        for book in books:
            book_mongo = BookMongo(**book.book.dict())
            book_json = book_mongo.dict(by_alias=True)
            _books.append(book_json)

        start_time = time.time()
        self.collection = self.db.get_collection("books")
        self.collection.insert_many(_books)
        end_time = time.time()

       
        return (end_time-start_time)*1000

    def delete(self, count: int):

        collections = self.collection.find({}).limit(count)
        ids: t.List[any] = []
        for entity in collections:
            ids.append(entity['_id'])

        start_time = time.time()
        result = self.collection.delete_many({"_id": {"$in": ids}})
        end_time = time.time()

        return (end_time-start_time)*1000

    def filter_test_1(self):
        self.collection = self.db.get_collection("books")
        query = {"pages": {"$gt": 100, "$lt": 200}}
        start_time = time.time()
        all_documents = self.collection.find(query)
        end_time = time.time()

        counter = 0
        for document in all_documents:
            counter += 1
        return [counter, (end_time-start_time)*1000]
    
    def filter_test_2(self):
        categories = ["dramat", "komedia", "tragedia", "horror", "fantasy", "historia", "romans"]
        self.collection = self.db.get_collection("books")
        query = {"categories.name": {"$in": categories}, "lang": "polski", "pages": {"$gt": 100, "$lt": 200}, "quotes.content": {"$regex" : "to"}}
        start_time = time.time()
        all_documents = self.collection.find(query)
        end_time = time.time()

        
        counter = 0
        for document in all_documents:
            counter += 1
        return [counter, (end_time-start_time)*1000, "SELECT * FROM categories JOIN books ON categories.book_id = books.id JOIN quotes ON quotes.book_id = books.id WHERE books.lang = 'polski' AND books.pages > 100 AND books.pages < 200 AND quotes.content LIKE 'to'"]

    def clear_db(self):
        self.db.drop_collection("books")
        self.db.drop_collection("categories")
        self.db.drop_collection("comments")
        self.db.drop_collection("quotes")
