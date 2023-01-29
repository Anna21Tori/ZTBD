from dataclasses import dataclass
from app.repository import RepositoryMongo, RepositorySql, Book, RepositoryDAO, RepositoryRedis
from loader_data import load_all_records
import typing as t
import json
import argparse


@dataclass
class AddTestItem:
    num_records: int
    time: t.List[float]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


@dataclass
class AddTest:
    test: t.List[AddTestItem]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


def get_repository(db: str) -> RepositoryDAO:
    if db == "mongodb":
        return RepositoryMongo()
    if db == "postgresql":
        return RepositorySql()
    if db == "redis":
        return RepositoryRedis()


#without comments, categories and quotes
def add_only_books_test(db):
    dao = get_repository(db)
    dao.clear_db()
    records: t.List[Book] = load_all_records()
    times = [1, 10, 100, 1000, 10000, 50000, 100000, 150000, 200000, 250000, 300000]
    all_measurement: AddTest =  AddTest(test=[])
    for t in times:
        measurement: AddTestItem = AddTestItem(num_records=t, time=[])
        for _ in range (0, 3):
            dao.clear_db()
            time = dao.save(records[0: t+1])
            measurement.time.append(time)
        all_measurement.test.append(measurement)
        print(db+ " "+ str(t))

    with open(f'add_test_{db}.json', 'w') as outfile:
        outfile.write(all_measurement.to_json())


#with comment, categories and quotes
def add_books_test_all(db):
    dao = get_repository(db)
    dao.clear_db()
    records: t.List[Book] = load_all_records()
    times = [1, 10, 100, 1000, 10000]
    all_measurement: AddTest =  AddTest(test=[])
    for t in times:
        measurement: AddTestItem = AddTestItem(num_records=t, time=[])
        for _ in range (0, 3):
            dao.clear_db()
            time = dao.save_all(records[0: t+1])
            measurement.time.append(time)
        all_measurement.test.append(measurement)
        print(db+ " "+ str(t))

    with open(f'add_test_{db}_all.json', 'w') as outfile:
        outfile.write(all_measurement.to_json())


def del_books_test(db):
    dao = get_repository(db)
    dao.clear_db()
    records: t.List[Book] = load_all_records()
    times = [1, 100, 1000]
    all_measurement: AddTest =  AddTest(test=[])
    for t in times:
        measurement: AddTestItem = AddTestItem(num_records=t, time=[])
        for _ in range (0, 3):
            dao.clear_db()
            dao.save_all(records)
            time = dao.delete(t)
            measurement.time.append(time)
        all_measurement.test.append(measurement)
        print(db+ " "+ str(t))

    with open(f'del_test_{db}.json', 'w') as outfile:
        outfile.write(all_measurement.to_json())


def filter_books_test(db):
    dao = get_repository(db)
    dao.clear_db()
    records: t.List[Book] = load_all_records()
    dao.save_all(records)
    all_measurement: AddTest =  AddTest(test=[])
    measurement1: AddTestItem = AddTestItem(num_records=0, time=[])
    for _ in range (0, 10):
        result = dao.filter_test_1()
        print(result[1])
        measurement1.time.append(result[1])
        measurement1.num_records = result[0]
    all_measurement.test.append(measurement1)

    measurement2: AddTestItem = AddTestItem(num_records=0, time=[])
    for _ in range (0, 10):
        result = dao.filter_test_2()
        print(result[1])
        measurement2.time.append(result[1])
        measurement2.num_records = result[0]
    all_measurement.test.append(measurement2)

    measurement3: AddTestItem = AddTestItem(num_records=0, time=[])
    for _ in range (0, 10):
        result = dao.filter_test_3()
        print(result[1])
        measurement3.time.append(result[1])
        measurement3.num_records = result[0]
    all_measurement.test.append(measurement3)

    with open(f'filter_test_{db}.json', 'w') as outfile:
        outfile.write(all_measurement.to_json())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test")
    args = parser.parse_args()

    if args.test == "add_books_mongo":
        add_only_books_test("mongodb")
    if args.test == "add_books_redis":
        add_only_books_test("redis")
    if args.test == "add_books_postgresql":
        add_only_books_test("postgresql")
    if args.test == "add_books_mongo_all":
        add_books_test_all("mongodb")
    if args.test == "add_books_postgresql_all":
        add_books_test_all("postgresql")
    if args.test == "add_books_redis_all":
        add_books_test_all("redis")
    if args.test == "del_books_mongo":
        del_books_test("mongodb")
    if args.test == "del_books_postgresql":
         del_books_test("postgresql")
    if args.test == "del_books_redis":
         del_books_test("redis")
    if args.test == "filter_books_mongo":
        filter_books_test("mongodb")
    if args.test == "filter_books_postgresql":
        filter_books_test("postgresql")
