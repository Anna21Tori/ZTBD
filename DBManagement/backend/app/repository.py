from abc import ABC, abstractmethod
from app.models.book.book import BookDB, BookMongo, BookCreate
from app.models.comment.comment import CommentDB, CommentMongo, CommentCreate
from app.models.quote.quote import QuoteDB, QuoteMongo, QuoteCreate
from app.models.category.category import CategoryDB, CategoryMongo, CategoryCreate
from app.databases.sql import SessionLocal, Base, engine
from app.databases.mongo import db as mongodb
import typing as t
from dataclasses import dataclass

@dataclass
class Repository:
    books: t.List[BookCreate]
    comments: t.List[CommentCreate]
    quotes: t.List[QuoteCreate]
    categories: t.List[CategoryCreate]

class RepositoryDAO(ABC):
    @abstractmethod
    def save(self, repo: Repository):
        pass
    @abstractmethod
    def delete(self, repo: Repository):
        pass
    @abstractmethod
    def clear_db(self):
        pass

class RepositorySql(RepositoryDAO):

    def __init__(self) -> None:
        super().__init__()
        self.session = SessionLocal()

    def save(self, repo: Repository):
        for book in repo.books:
            _book = BookDB(**book.dict())
            self.session.add(_book)

        for category in repo.categories:
            _category = CategoryDB(**category.dict())
            self.session.add(_category)
                    
        for comment in repo.comments:
            _comment = CommentDB(**comment.dict())
            self.session.add(_comment)
                
        for quote in repo.quotes:
            _quote = QuoteDB(**quote.dict())
            self.session.add(_quote)

        self.session.commit()
    
    
    def delete(self, repo: Repository):
        for book in repo.books:
            #_book = BookDB(**book.dict())
            _book = self.session.query(BookDB).filter_by(id = book.id).first()
            self.session.delete(_book)

        self.session.commit()


    def find(self):
        # 1
        # query = self.session.query(BookDB).filter(BookDB.pages > 100, BookDB.pages < 200)
        # print(f"Count: {query.count()}")

        # 2
        # cat = ["dramat", "komedia", "romans", "tragedia"]
        # subquery = self.session.query(CategoryDB.book_id).filter(CategoryDB.name not in cat).subquery()
        # query = self.session.query(BookDB).filter(BookDB.id.in_(subquery))
        # print(f"Count: {query.count()}")

        # 3
        # query = self.session.query(BookDB).filter(BookDB.lang != "polski")
        # print(f"Count: {query.count()}")

        # 4
        # query = self.session.query(BookDB).filter(BookDB.author.contains("jan"))
        # print(f"Count: {query.count()}")

        # 5
        subquery = self.session.query(QuoteDB.book_id).filter(QuoteDB.content.contains("co")).subquery()
        query = self.session.query(BookDB).filter(BookDB.id.in_(subquery))
        print(f"Count: {query.count()}")



        # self.collection = self.db.get_collection("books")
        # query = {"pages": {"$gt": 100, "$lt": 200}}
        # all_documents = self.collection.find(query)
        # counter = 0
        # for document in all_documents:
        #     counter += 1
        #     # print(document)
        # print(f"Counter: {counter}")


    def clear_db(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

class RepositoryMongo(RepositoryDAO):

    def __init__(self) -> None:
        super().__init__()
        self.db = mongodb
        #self.collection = self.db.get_collection("books")


    def save(self, repo: Repository):
        for book in repo.books:
            self.collection = self.db.get_collection("books")
            book_mongo = BookMongo(**book.dict())
            book_json = book_mongo.dict(by_alias=True)
            book_id = self.collection.insert_one(book_json).inserted_id

        for category in repo.categories:
            self.collection = self.db.get_collection("categories")
            category.book_id = book_id
            category_mongo = CategoryMongo(**category.dict())
            category_json = category_mongo.dict(by_alias=True)
            self.collection.insert_one(category_json).inserted_id

        for comment in repo.comments:
            self.collection = self.db.get_collection("comments")
            comment.book_id = book_id
            comment_mongo = CommentMongo(**category.dict())
            comment_json = comment_mongo.dict(by_alias=True)
            self.collection.insert_one(comment_json).inserted_id

        for quote in repo.quotes:
            self.collection = self.db.get_collection("quotes")
            quote.book_id = book_id
            quote_mongo = QuoteMongo(**category.dict())
            quote_json = quote_mongo.dict(by_alias=True)
            self.collection.insert_one(quote_json).inserted_id

    def delete(self, repo: Repository):
        result = self.collection.delete_many({})
        # print(result.acknowledged, result.deleted_count)
            #self.collection = self.db.get_collection("books")
            #book_mongo = BookMongo(**book.dict())
            #book_json = book_mongo.dict(by_alias=True)
            # book_id = self.collection.insert_one(book_json).inserted_id
            # result = self.collection.delete_one({})
            # print(result.acknowledged, result.deleted_count)


    def find(self):
        self.collection = self.db.get_collection("books")
        query = {"pages": {"$gt": 100, "$lt": 200}}
        all_documents = self.collection.find(query)
        counter = 0
        for document in all_documents:
            counter += 1
            # print(document)
        print(f"Counter: {counter}")

    def clear_db(self):
        self.db.drop_collection("books")
        self.db.drop_collection("categories")
        self.db.drop_collection("comments")
        self.db.drop_collection("quotes")
