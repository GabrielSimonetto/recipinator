"""There are plenty of ways to do this using the TACO api

https://github.com/raulfdm/taco-api

I'll do the laziest and most error prone for now.

I couldn't find where in the official source they defined the units for these values
  but it seems like it is always 100g: https://taco-food-api.herokuapp.com/api/v1/food
"""

import pandas as pd

CSV_URL = 'https://raw.githubusercontent.com/raulfdm/taco-api/master/references/TACO_formatted.csv'
TARGET_COLUMNS = ['description', 'energy_kcal', 'protein_g', 'lipid_g', 'carbohydrate_g', 'fiber_g']

COLS = {
    'name':             'description',
    'calories':         'energy_kcal',
    'carbohydrate':     'carbohydrate_g',
    'protein':          'protein_g',
    'fat':              'lipid_g',
    'fiber':            'fiber_g',
}

DTYPES = {
    'description':        'object',
    'energy_kcal':        'float64',
    'carbohydrate_g':     'float64',
    'protein_g':          'float64',
    'lipid_g':            'float64',
    'fiber_g':            'float64',
}


# This should probably be used on searches aswell
# but then it would need to be a version for strings and not series, of course.
# AND, the other tables need this aswell
def normalize_text(s):
    '''Normalizes a series of texts'''
    return (s.str.normalize('NFKD')
                .str.encode('ascii', errors='ignore')
                .str.decode('utf-8')
                .str.lower()
                .str.strip())                


def get_nutrient_information():
    dataframe = pd.read_csv(CSV_URL, usecols=TARGET_COLUMNS)
    dataframe[COLS['name']] = normalize_text(dataframe[COLS['name']])
    dataframe.index.name = 'id'
    dataframe.index += 1

    for col, dtype in DTYPES.items():
      if dtype == 'float64':
        dataframe[col] = pd.to_numeric(dataframe[col], errors='coerce')
        dataframe[col] = dataframe[col].round(decimals=2)

    return dataframe

