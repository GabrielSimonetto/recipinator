import json

from recipinator import DATA_PATH

def get_scraped_data(path = DATA_PATH) -> list:
    with open(path) as file:
        return json.load(file)
