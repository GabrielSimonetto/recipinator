from dataclasses import dataclass

@dataclass
class Recipe:
    recipe_id: int
    name: str
    link: str = None
    owner: int = None

    def __str__(self):
        if self.link != None:
            return f"Receita de ID:{self.recipe_id}; {self.name}: {self.link}"
        else:
            return f"Receita de ID:{self.recipe_id}; {self.name}: adicionado por usuário."

    def __repr__(self):
        if self.link != None:
            return f"Receita de ID:{self.recipe_id}; {self.name}: {self.link}"
        else:
            return f"Receita de ID:{self.recipe_id}; {self.name}: adicionado por usuário."

    def get_recipe_id(self):
        return self.recipe_id
