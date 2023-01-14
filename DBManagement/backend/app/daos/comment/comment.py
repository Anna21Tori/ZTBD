from abc import ABC, abstractmethod
from app.databases.sql import Session
from app.models.comment.comment import CommentDB, Comment, CommentCreate, CommentMongo
from fastapi import Depends
from app.databases.sql import get_session
from typing import Optional

from app.databases.mongo import db as mongodb
from pymongo.database import Database
import typing as t


class CommentDAO(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Comment]:
        pass

    @abstractmethod
    def save(self, comment: CommentCreate) -> Comment:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

def get_dao(db:str, session: Session = Depends(get_session)):
    if db == "postgresql":
        dao = CommentDAOSql(session)
        yield dao
    elif db == "mongodb":
        dao = CommentDAOMongo(mongodb)
        yield dao
    else:
        raise NotImplementedError()
    

class CommentDAOSql(CommentDAO):

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def get_by_id(self, id: str) -> Optional[Comment]:
        comment_sql = self.session.query(CommentDB).filter(CommentDB.id == id).first()
        if not comment_sql:
            return None
        return Comment.from_orm(comment_sql)

    def save(self, comment: CommentCreate):
        comment_sql = CommentDB(**comment.dict())
        self.session.add(comment_sql)
        self.session.commit()
        self.session.refresh(comment_sql)
        return Comment.from_orm(comment_sql)
    def delete(self, id: str):
        comment_sql = self.session.query(CommentDB).filter(CommentDB.id == id).first()
        self.session.delete(comment_sql)

class CommentDAOMongo(CommentDAO):

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self.collection = db.get_collection("comments")

    def get_by_id(self, id: str) -> t.Optional[Comment]:
        model_bson = self.collection.find_one({'id': id})
        if model_bson:
            model_mongo = CommentMongo(**model_bson)

            return Comment.from_orm(model_mongo)
        else:
            return None

    def save(self, model_create: CommentCreate) -> Comment:
        model_mongo = CommentMongo(**model_create.dict())
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
