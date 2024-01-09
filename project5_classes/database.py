from .relation import Relation
from typing import Dict

class Database:
    def __init__(self, database: Dict[str, Relation] = {}) -> None:
        self.relations = database