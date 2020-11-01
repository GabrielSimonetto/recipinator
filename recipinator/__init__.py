from pathlib import Path

PROJECT_NAME = 'recipinator'
DB_NAME = 'recipinator.db'
RECIPE_TABLE_NAME = 'recipes'
INGREDIENTS_TABLE_NAME = 'ingredients'
FAVORITE_TABLE_NAME = 'favorites'
USER_TABLE_NAME = 'users'

ROOT = Path(__file__).parents[1]
SRC_PATH = ROOT / PROJECT_NAME
SCRAPERS_PATH = SRC_PATH / 'scrapers'
DATA_PATH = SCRAPERS_PATH / 'data.json'
DB_PATH = SRC_PATH / 'database' / DB_NAME
