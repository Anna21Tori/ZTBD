from abc import ABC, abstractmethod
from app.databases.sql import Session
from app.models.quote.quote import QuoteDB, Quote, QuoteCreate, QuoteMongo
from fastapi import Depends
from app.databases.sql import get_session
from typing import Optional

from app.databases.mongo import db as mongodb
from pymongo.database import Database
import typing as t


class QuoteDAO(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Quote]:
        pass

    @abstractmethod
    def save(self, quote: QuoteCreate) -> Quote:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

def get_dao(db:str, session: Session = Depends(get_session)):
    if db == "postgresql":
        dao = QuoteDAOSql(session)
        yield dao
    elif db == "mongodb":
        dao = QuoteDAOMongo(mongodb)
        yield dao
    else:
        raise NotImplementedError()
    

class QuoteDAOSql(QuoteDAO):

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def get_by_id(self, id: str) -> Optional[Quote]:
        quote_sql = self.session.query(QuoteDB).filter(QuoteDB.id == id).first()
        if not quote_sql:
            return None
        return Quote.from_orm(quote_sql)

    def save(self, quote: QuoteCreate):
        quote_sql = QuoteDB(**quote.dict())
        self.session.add(quote_sql)
        self.session.commit()
        self.session.refresh(quote_sql)
        return Quote.from_orm(quote_sql)
    def delete(self, id: str):
        quote_sql = self.session.query(QuoteDB).filter(QuoteDB.id == id).first()
        self.session.delete(quote_sql)

class QuoteDAOMongo(QuoteDAO):

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self.collection = db.get_collection("quotes")

    def get_by_id(self, id: str) -> t.Optional[Quote]:
        model_bson = self.collection.find_one({'id': id})
        if model_bson:
            model_mongo = QuoteMongo(**model_bson)

            return Quote.from_orm(model_mongo)
        else:
            return None

    def save(self, model_create: QuoteCreate) -> Quote:
        model_mongo = QuoteMongo(**model_create.dict())
        model_json = model_mongo.dict(by_alias=True)
        if self.get_by_id(model_mongo.id):
            raise ValueError("Exists!")
        self.collection.insert_one(model_json)
        ret = self.get_by_id(model_create.id)
        if not ret:
            raise ValueError("Couldn't get after add!") 
        else:
            return ret

    def delete(self, id: str):
        raise NotImplementedError()
