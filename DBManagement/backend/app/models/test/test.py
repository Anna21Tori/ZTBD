from dataclasses import dataclass
import typing as t
import json

@dataclass
class AddTestItem:
    num_records: int
    time: t.List[float]

    @classmethod
    def from_json(self, data: dict):
        return self(**data)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    def __init__(self, **entries):
        self.__dict__.update(entries)


@dataclass
class AddTest:
    test: t.List[AddTestItem]

    @classmethod
    def from_json(self, data: dict):
        test = map(AddTestItem.from_json, data["test"])
        return self(test=test)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __init__(self, **entries):
        self.__dict__.update(entries)

@dataclass
class ResultTest:
    mongodb: AddTest
    postgresql: AddTest
    redis: AddTest

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

@dataclass
class ResultFiltersTest:
    sqls: t.List[str]
    mongodb: AddTest
    postgresql: AddTest
    redis: AddTest

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)