from abc import ABC, abstractmethod
from app.databases.sql import Session
from app.models.book.book import BookDB, BookMongo, Book, BookCreate
from fastapi import Depends
from app.databases.sql import get_session
from pymongo.database import Database
from app.databases.mongo import db as mongodb
import typing as t

class BookDAO(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Book:
        pass

    @abstractmethod
    def save(self, book: BookCreate) -> Book:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

def get_dao(db: str, session: Session = Depends(get_session)):
    if db == "postgresql":
        dao = BookDAOSql(session)
        yield dao
    elif db == "mongodb":
        dao = BookDAOMongo(mongodb)
        yield dao
    else:
        raise NotImplementedError()

class BookDAOSql(BookDAO):

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def get_by_id(self, id: str) -> Book:
        book_sql = self.session.query(BookDB).filter(BookDB.id == id).first()
        return Book.from_orm(book_sql)

    def save(self, book: BookCreate):
        book_sql = BookDB(**book.dict())
        self.session.add(book_sql)
        self.session.commit()
        self.session.refresh(book_sql)
        return Book.from_orm(book_sql)
    def delete(self, id: str):
        book_sql = self.session.query(BookDB).filter(BookDB.id == id).first()
        self.session.delete(book_sql)


class BookDAOMongo(BookDAO):

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self.collection = db.get_collection("books")

    def get_by_id(self, id: str) -> t.Optional[Book]:
        book_bson = self.collection.find_one({'id': id})
        if book_bson:

            book_mongo = BookMongo(**book_bson)

            return Book.from_orm(book_mongo)
        else:
            return None

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

    def delete(self, id: str):
        raise NotImplementedError()