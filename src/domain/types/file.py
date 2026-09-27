from dataclasses import dataclass


@dataclass
class FileData:
    id: str
    name: str
    url: str
    assignment_id: str