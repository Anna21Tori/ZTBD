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
    mongodb = RepositoryMongo()
    postgresql = RepositorySql()
    mongodb.clear_db()
    postgresql.clear_db()
    records: Repository = load_all_records()
    times = [1, 10, 100, 1000, 10000]
    all_measurement: AddTest = AddTest(mongodb=[], postgresql=[])
    
    for db in ["mongodb", "postgresql"]:
        if db == "mongodb":
            for t in times:
                measurement: AddTestItem = AddTestItem(num_records=t, time=[])
                for _ in range (0, 3):
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
                for _ in range (0, 3):
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

def delete_books_test():
    mongodb = RepositoryMongo()
    postgresql = RepositorySql()
    mongodb.clear_db()
    postgresql.clear_db()
    records: Repository = load_all_records()
    times = [1, 10, 100, 1000, 10000]
    all_measurement: AddTest = AddTest(mongodb=[], postgresql=[])
    
    for db in ["mongodb", "postgresql"]:
        if db == "mongodb":
            for t in times:
                measurement: AddTestItem = AddTestItem(num_records=t, time=[])
                for _ in range (0, 3):
                    mongodb.clear_db()
                    repo: Repository = Repository(books=records.books[0: t+1], categories=[], quotes=[], comments=[])
                    mongodb.save(repo)
                    start_time = time.time()
                    mongodb.delete(repo)
                    end_time = time.time()
                    measurement.time.append(end_time-start_time)
                all_measurement.mongodb.append(measurement)
                print(db+ " "+ str(t))
        if db == "postgresql":
            for t in times:
                measurement: AddTestItem = AddTestItem(num_records=t, time=[])
                for _ in range (0, 3):
                    postgresql.clear_db()
                    repo: Repository = Repository(books=records.books[0: t+1], categories=[], quotes=[], comments=[])
                    postgresql.save(repo)
                    start_time = time.time()
                    postgresql.delete(repo)
                    end_time = time.time()
                    measurement.time.append(end_time-start_time)
                all_measurement.postgresql.append(measurement)
                print(db+ " "+ str(t))

    with open('delete_test.json', 'w') as outfile:
        outfile.write(all_measurement.to_json())


def find_books_test():
    mongodb = RepositoryMongo()
    postgresql = RepositorySql()
    mongodb.clear_db()
    postgresql.clear_db()
    records: Repository = load_all_records()
    times = [1, 10, 100, 1000, 10000]
    all_measurement: AddTest = AddTest(mongodb=[], postgresql=[])
    
    for db in ["mongodb", "postgresql"]:
        if db == "mongodb":
            for t in times:
                measurement: AddTestItem = AddTestItem(num_records=t, time=[])
                for _ in range (0, 3):
                    mongodb.clear_db()
                    repo: Repository = Repository(books=records.books[0: t+1], categories=[], quotes=[], comments=[])
                    mongodb.save(repo)
                    start_time = time.time()
                    mongodb.find()
                    end_time = time.time()
                    measurement.time.append(end_time-start_time)
                all_measurement.mongodb.append(measurement)
                print(db+ " "+ str(t))
        if db == "postgresql":
            for t in times:
                measurement: AddTestItem = AddTestItem(num_records=t, time=[])
                for _ in range (0, 3):
                    postgresql.clear_db()
                    repo: Repository = Repository(books=records.books[0: t+1], categories=records.categories[0: t+1], quotes=records.quotes[0: t+1], comments=records.comments[0: t+1])
                    postgresql.save(repo)
                    start_time = time.time()
                    postgresql.find()
                    end_time = time.time()
                    measurement.time.append(end_time-start_time)
                all_measurement.postgresql.append(measurement)
                print(db+ " "+ str(t))

    with open('query1_test.json', 'w') as outfile:
        outfile.write(all_measurement.to_json())


if __name__ == "__main__":
    # add_books_test()
    # delete_books_test()
    find_books_test()
