from dataclasses import dataclass

@dataclass
class Task:
    title: str
    description: str
    priority: int = 1
    completed: bool = False

@dataclass
class Idea:
    title: str
    benefit: str
    cost: str
