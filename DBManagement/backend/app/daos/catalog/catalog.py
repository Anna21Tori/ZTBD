from abc import ABC, abstractmethod
from app.databases.sql import Session
from app.models.book.book import BookDB, BookMongo, Book, BookCreate
from app.models.comment.comment import CommentDB
from app.models.quote.quote import QuoteDB
from app.models.category.category import CategoryDB
from app.models.catalog.catalog import CatalogCreate
from fastapi import Depends
from app.databases.sql import get_session
from pymongo.database import Database
from app.databases.mongo import db as mongodb
import typing as t

class CatalogDAO(ABC):

    @abstractmethod
    def save(self, catalog: t.List[CatalogCreate]):
        pass


def get_dao(db: str, session: Session = Depends(get_session)):
    if db == "postgresql":
        dao = CatalogDAOSql(session)
        yield dao
    elif db == "mongodb":
        dao = CatalogDAOMongo(mongodb)
        yield dao
    else:
        raise NotImplementedError()

class CatalogDAOSql(CatalogDAO):

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def save(self, catalog: t.List[CatalogCreate]):
        for item in catalog:
            
            book_sql = BookDB(**item.book.dict())
            self.session.add(book_sql)
            self.session.commit()
            self.session.refresh(book_sql)
            
            book_id = book_sql.id
            
            for category in item.categories:
                category.book_id = book_id
                category_sql = CategoryDB(**category.dict())
                self.session.add(category_sql)
                self.session.commit()
                self.session.refresh(category_sql)
                
            for comment in item.comments:
                comment.book_id = book_id
                comment_sql = CategoryDB(**comment.dict())
                self.session.add(comment_sql)
                self.session.commit()
                self.session.refresh(comment_sql)
                
            for quote in item.quotes:
                quote.book_id = book_id
                quote_sql = CategoryDB(**quote.dict())
                self.session.add(quote_sql)
                self.session.commit()
                self.session.refresh(quote_sql)
            
            
            



class CatalogDAOMongo(CatalogDAO):

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self.collection = db.get_collection("books")


    def save(self, book: BookCreate) -> Book:
        book_mongo = BookMongo(**book.dict())
        book_json = book_mongo.dict(by_alias=True)
        if self.get_by_id(book.id):
            raise ValueError("Exists!")
        self.collection.insert_one(book_json).inserted_id
        ret = self.get_by_id(book.id)
        if not ret:
            raise ValueError("Couldn't get after add") 
        else:
            return ret
