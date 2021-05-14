from enum import Enum, auto

class ValidRoles(Enum):
    reader = auto()
    writer = auto()
    admin = auto()