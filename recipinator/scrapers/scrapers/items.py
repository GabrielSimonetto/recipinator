# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
from w3lib.html import remove_tags

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def remove_whitespace(value):
    return value.strip()

def clean_title(raw_string):
    return re.search(r"\n.*\n", raw_string).group().strip('\n')

class TitleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(remove_tags, remove_whitespace),
        output_processor = TakeFirst()
    )