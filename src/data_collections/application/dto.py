from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class CollectionDTO:
    id: int
    edited: str
    filename: str

@dataclass
class DatasetDTO:
    filename: str
    headers: List
    dataset: Dict
    records: int
    filters: Tuple