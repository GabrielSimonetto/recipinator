from dataclasses import dataclass

@dataclass
class Nutrient:
    id: int
    description: str
    energy_kcal: float
    protein_g: float
    lipid_g: float
    carbohydrate_g: float
    fiber_g: float

    def __str__(self):
        return f"Receita de ID:{self.id};\nDescrição: {self.description},\nCalorias(kcal): {self.energy_kcal},\nProteina(g): {self.protein_g},\nLipidios(g): {self.lipid_g},\nCarboidratos(g): {self.carbohydrate_g},\nFibra(g): {self.fiber_g}"

    def __repr__(self):
        return f"Receita de ID:{self.id};\nDescrição: {self.description},\nCalorias(kcal): {self.energy_kcal},\nProteina(g): {self.protein_g},\nLipidios(g): {self.lipid_g},\nCarboidratos(g): {self.carbohydrate_g},\nFibra(g): {self.fiber_g}"


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
