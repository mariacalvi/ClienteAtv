from dataclasses import dataclass
from typing import Optional


@dataclass
class Costumer:
    id: Optional[int] = None
    name: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None