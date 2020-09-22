# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


def remove_whitespace(value):
    return value.strip()


class RecipeItem(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(remove_tags, remove_whitespace),
        output_processor = TakeFirst()
    )
    ingredient_list = scrapy.Field(
        input_processor = MapCompose(remove_tags, remove_whitespace),
        output_processor = TakeFirst()
    )

