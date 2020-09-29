from dataclasses import dataclass

@dataclass
class Recipe:
    recipe_id: int
    name: str
    link: str

    def __str__(self):
        return f"{self.name}: {self.link}"

    def __repr__(self):
        return f"{self.name}: {self.link}"


