from abc import ABC, abstractmethod
from app.databases.sql import Session
from app.models.book.book import BookDB, BookMongo, Book, BookCreate
from app.models.comment.comment import CommentDB, CommentMongo, CommentCreate
from app.models.quote.quote import QuoteDB, QuoteMongo, QuoteCreate
from app.models.category.category import CategoryDB, CategoryMongo, CategoryCreate
from fastapi import Depends
from app.databases.sql import SessionLocal
from pymongo.database import Database
from app.databases.mongo import db as mongodb
import typing as t
import logging
from dataclasses import dataclass

@dataclass
class Catalog:
    book: BookCreate
    comments: t.List[CommentCreate]
    quotes: t.List[QuoteCreate]
    categories: t.List[CategoryCreate]
class CatalogDAO(ABC):

    @abstractmethod
    def save(self, catalog: Catalog):
        pass
    @abstractmethod
    def get_by_id(self, id: str) -> Book:
        pass

class CatalogDAOSql(CatalogDAO):

    def __init__(self) -> None:
        super().__init__()
        self.session = SessionLocal()

    def save(self, item: Catalog):
        # db_session = get_session
        book_sql = BookDB(**item.book.dict())
        self.session.add(book_sql)
        self.session.commit()
        self.session.refresh(book_sql)
                
        book_id = Book.from_orm(book_sql).id
                
        for category in item.categories:
            category.book_id = book_id
            category_sql = CategoryDB(**category.dict())
            self.session.add(category_sql)
            self.session.commit()
            self.session.refresh(category_sql)
                    
        for comment in item.comments:
            comment.book_id = book_id
            comment_sql = CommentDB(**comment.dict())
            self.session.add(comment_sql)
            self.session.commit()
            self.session.refresh(comment_sql)
                
        for quote in item.quotes:
            quote.book_id = book_id
            quote_sql = QuoteDB(**quote.dict())
            self.session.add(quote_sql)
            self.session.commit()
            self.session.refresh(quote_sql)

        print(Book.from_orm(book_sql))

        self.session.close()

    def get_by_id(self, id: str) -> Book:
        book_sql = self.session.query(BookDB).filter(BookDB.id == id).first()
        return Book.from_orm(book_sql)

class CatalogDAOMongo(CatalogDAO):

    def __init__(self) -> None:
        super().__init__()
        self.db = mongodb
        self.collection = self.db.get_collection("books")


    def save(self, item: Catalog):

        self.collection = self.db.get_collection("books")
        book_mongo = BookMongo(**item.book.dict())
        book_json = book_mongo.dict(by_alias=True)
        book_id = self.collection.insert_one(book_json).inserted_id
            
        for category in item.categories:
            self.collection = self.db.get_collection("categories")
            category.book_id = book_id
            category_mongo = CategoryMongo(**category.dict())
            category_json = category_mongo.dict(by_alias=True)
            self.collection.insert_one(category_json).inserted_id
                
        for comment in item.comments:
            self.collection = self.db.get_collection("comments")
            comment.book_id = book_id
            comment_mongo = CommentMongo(**category.dict())
            comment_json = comment_mongo.dict(by_alias=True)
            self.collection.insert_one(comment_json).inserted_id
                
        for quote in item.quotes:
            self.collection = self.db.get_collection("quotes")
            quote.book_id = book_id
            quote_mongo = QuoteMongo(**category.dict())
            quote_json = quote_mongo.dict(by_alias=True)
            self.collection.insert_one(quote_json).inserted_id

    def get_by_id(self, id: str) -> t.Optional[Book]:
        book_bson = self.collection.find_one({'id': id})
        if book_bson:

            book_mongo = BookMongo(**book_bson)

            return Book.from_orm(book_mongo)
        else:
            return None
