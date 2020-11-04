from dataclasses import dataclass

@dataclass
class Recipe:
    recipe_id: int
    name: str
    link: str

    def __str__(self):
        return f"Receita de ID:{self.recipe_id}; {self.name}: {self.link}"

    def __repr__(self):
        return f"Receita de ID:{self.recipe_id}; {self.name}: {self.link}"

    def get_recipe_id(self):
        return self.recipe_id
