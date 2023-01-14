from abc import ABC, abstractmethod
from app.databases.sql import Session
from app.models.category.category import CategoryDB, Category, CategoryCreate, CategoryMongo
from fastapi import Depends
from app.databases.sql import get_session
from typing import Optional

from app.databases.mongo import db as mongodb
from pymongo.database import Database
import typing as t


class CategoryDAO(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Category]:
        pass

    @abstractmethod
    def save(self, category: CategoryCreate) -> Category:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

def get_dao(db:str, session: Session = Depends(get_session)):
    if db == "postgresql":
        dao = CategoryDAOSql(session)
        yield dao
    elif db == "mongodb":
        dao = CategoryDAOMongo(mongodb)
        yield dao
    else:
        raise NotImplementedError()
    

class CategoryDAOSql(CategoryDAO):

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def get_by_id(self, id: str) -> Optional[Category]:
        category_sql = self.session.query(CategoryDB).filter(CategoryDB.id == id).first()
        if not category_sql:
            return None
        return Category.from_orm(category_sql)

    def save(self, category: CategoryCreate):
        category_sql = CategoryDB(**category.dict())
        self.session.add(category_sql)
        self.session.commit()
        self.session.refresh(category_sql)
        return Category.from_orm(category_sql)
    def delete(self, id: str):
        category_sql = self.session.query(CategoryDB).filter(CategoryDB.id == id).first()
        self.session.delete(category_sql)

class CategoryDAOMongo(CategoryDAO):

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self.collection = db.get_collection("categories")

    def get_by_id(self, id: str) -> t.Optional[Category]:
        model_bson = self.collection.find_one({'id': id})
        if model_bson:
            model_mongo = CategoryMongo(**model_bson)

            return Category.from_orm(model_mongo)
        else:
            return None

    def save(self, model_create: CategoryCreate) -> Category:
        model_mongo = CategoryMongo(**model_create.dict())
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
