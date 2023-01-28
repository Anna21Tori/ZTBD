from dataclasses import dataclass
import typing as t
import json

@dataclass
class AddTestItem:
    num_records: int
    time: t.List[float]

    # def __init__(self, num_records: int, time: t.List[int]):
    #     self.num_records = num_records
    #     self.time = time

    # def __iter__(self):
    #     yield from {
    #         "num_records": self.num_records,
    #         "postgresql": self.time,
    #     }.items()

    # def __str__(self):
    #     return json.dumps(dict(self), ensure_ascii=False)

    # def __repr__(self):
    #     return self.__str__()

    @classmethod
    def from_json(self, data: dict):
        return self(**data)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    # @staticmethod
    # def from_json(json_dct):
    #   return AddTestItem(json_dct['num_records'],
    #                json_dct['time'])


@dataclass
class AddTest:
    mongodb: t.List[AddTestItem]
    postgresql: t.List[AddTestItem]

    # def __init__(self, mongodb: t.List[AddTestItem], postgresql: t.List[AddTestItem]):
    #     self.mongodb = mongodb
    #     self.postgresql = postgresql

    # def __iter__(self):
    #     yield from {
    #         "mongodb": self.mongodb,
    #         "postgresql": self.postgresql,
    #     }.items()

    # def __str__(self):
    #     return json.dumps(dict(self), ensure_ascii=False)

    # def __repr__(self):
    #     return self.__str__()

    @classmethod
    def from_json(self, data: dict):
        mongodb = map(AddTestItem.from_json, data["mongodb"])
        postgresql = map(AddTestItem.from_json, data["postgresql"])
        return self(mongodb=mongodb, postgresql=postgresql)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    # @staticmethod
    # def from_json(json_dct):
    #     print(json_dct)
    #     return AddTest(json_dct['mongodb'],
    #                json_dct['postgresql'])