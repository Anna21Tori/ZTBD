from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import csv
from dataclasses import dataclass
from app.repository import RepositoryMongo, RepositorySql, Repository
from loader_data import load_all_records
import typing as t
import json
import time

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

def add_books_test():
    import typing as t
    mongodb = RepositoryMongo()
    postgresql = RepositorySql()

    mongodb.clear_db()
    postgresql.clear_db()

    records: Repository = load_all_records()
    
                        
    times = [1, 10, 100, 1000, 10000, 20000, 50000, 100000, 150000, 200000, 250000, 300000]


    all_measurement: AddTest = AddTest(mongodb=[], postgresql=[])
    
    for db in ["mongodb", "postgresql"]:
        if db == "mongodb":
            for t in times:
                measurement: AddTestItem = AddTestItem(num_records=t, time=[])
                for n in (0, 3, 1):
                    mongodb.clear_db()
                    repo: Repository = Repository(books=records.books[0: t+1], categories=[], quotes=[], comments=[])

                    start_time = time.time()
                    mongodb.save(repo)
                    end_time = time.time()

                    measurement.time.append(end_time-start_time)
                all_measurement.mongodb.append(measurement)
                print(db+ " "+ str(t))
        if db == "postgresql":
            for t in times:
                measurement: AddTestItem = AddTestItem(num_records=t, time=[])
                for n in (0, 3, 1):
                    postgresql.clear_db()
                    repo: Repository = Repository(books=records.books[0: t+1], categories=[], quotes=[], comments=[])
                    start_time = time.time()
                    postgresql.save(repo)
                    end_time = time.time()
                    measurement.time.append(end_time-start_time)
                all_measurement.postgresql.append(measurement)
                print(db+ " "+ str(t))
                
    with open('add_test.json', 'w') as outfile:
        outfile.write(all_measurement.to_json())           

if __name__ == "__main__":

    add_books_test()     
