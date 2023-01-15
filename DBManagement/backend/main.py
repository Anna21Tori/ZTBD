from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import csv
from dataclasses import dataclass
from app.core.config import settings
from app.databases import sql
from app.models.book.book import BookCreate
from app.models.comment.comment import CommentCreate
from app.models.quote.quote import QuoteCreate
from app.models.category.category import CategoryCreate
from app.daos.catalog.catalog import CatalogDAOMongo, CatalogDAOSql
import typing as t
import datetime 
import json
import time

@dataclass
class Catalog:
    book: BookCreate
    comments: t.List[CommentCreate]
    quotes: t.List[QuoteCreate]
    categories: t.List[CategoryCreate]

@dataclass
class AddTestItem:
    num_records: int
    time: t.List[int]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

@dataclass
class AddTest:
    mongodb: t.List[AddTestItem]
    postgresql: t.List[AddTestItem]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def get_test():

    mongodb = CatalogDAOMongo()
    postgresql = CatalogDAOSql()
    
    print(mongodb.get_by_id(id=0))
    print(postgresql.get_by_id(id=15))

def add_test():
    import typing as t
    book_id = 2
    comment_id = 10
    quote_id = 10
    category_id = 10
    records: t.List[Catalog] = []
    
    for file in os.listdir("./storage"):
        with open(f"./storage/{file}", encoding="utf8") as file_obj:
            print(file)
            heading = next(file_obj)
            reader_obj = csv.reader(file_obj)

            for row in reader_obj:
                title = row[0].strip()
                author = row[1].strip()
                categories = []
                if row[2] != '':
                    categories = row[2].strip().split(sep=',')
                publishing = row[3].strip()
                isbn = row[4].strip()
                description = row[5].strip()
                originalTitle = row[6].strip()
                _date = None
                if row[7] != '':
                    data = row[7].strip().split(sep="-")
                    _date = datetime.datetime(year=int(data[0]), month=int(data[1]), day=int(data[2]))
                datePol = None
                if row[8] != '':
                    data = row[8].strip().split(sep="-")
                    datePol = datetime.datetime(year=int(data[0]), month=int(data[1]), day=int(data[2]))
                pages = 0
                if row[9] != '':
                    pages = int(row[9].strip())
                lang = row[10].strip()
                translator = row[11].strip()
                comments = []
                if row[12] != '':
                    comments = row[12].strip().split(sep=',')
                quotes = []
                if row[13] != '':
                    quotes = row[13].strip().split(sep=',')
                            
                _book: BookCreate = BookCreate(
                                                id= book_id,
                                                title=title, 
                                                description=description, 
                                                isbn=isbn, 
                                                publishing=publishing, 
                                                author=author, 
                                                orginal_name=originalTitle, 
                                                date=_date, 
                                                pol_date=datePol, 
                                                pages=pages, 
                                                lang=lang, 
                                                translator=translator)
                book_id += 1

                _comments: t.List[CommentCreate] = []
                for comment in comments:
                    if comment != "":
                        _comments.append(CommentCreate(content=comment, id=comment_id))
                        comment_id +=1
                                
                _quotes: t.List[QuoteCreate] = []
                for quote in quotes:
                    if quote != "":
                        _quotes.append(CommentCreate(content=quote, id=quote_id))
                        quote_id += 1
                                
                _categories: t.List[CategoryCreate] = []
                for category in categories:
                    if category != '':
                            _categories.append(CategoryCreate(name=category, id=category_id))
                            category_id += 1

                catalog: Catalog = Catalog(
                    book = _book,
                    comments=_comments,
                    categories=_categories,
                    quotes=_quotes
                    )
                records.append(catalog)
                        
    times = [1, 10, 100, 1000, 10000]
    counter = 0

    

    all_measurement: AddTest = AddTest(mongodb=[], postgresql=[])
    for db in ["mongodb", "postgresql"]:
        if db == "mongodb":
            mongodb = CatalogDAOMongo()
            for t in times:
                measurement: AddTestItem = AddTestItem(num_records=t, time=[])
                for n in (0, 3, 1):
                    start = time.time()
                    for i in range(counter, counter+t, 1):
                        mongodb.save(records[i])
                    end = time.time()
                    measurement.time.append(end-start)
                all_measurement.mongodb.append(measurement)
        counter = 0
        if db == "postgresql":
            postgresql = CatalogDAOSql()
            for t in times:
                measurement: AddTestItem = AddTestItem(num_records=t, time=[])
                for n in (0, 3, 1):
                    start = time.time()
                    for i in range(counter, counter+t, 1):
                        postgresql.save(records[i])
                    end = time.time()
                    measurement.time.append(end-start)
                all_measurement.postgresql.append(measurement)
                
    with open('add_test.json', 'w') as outfile:
        outfile.write(all_measurement.to_json())           

if __name__ == "__main__":

    add_test()     
