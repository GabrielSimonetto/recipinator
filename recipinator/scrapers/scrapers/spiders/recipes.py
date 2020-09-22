import scrapy
from scrapers.items import TitleItem
from scrapy.loader import ItemLoader

# https://www.youtube.com/watch?v=Wp6LRijW9wg
# ^ referencia usada ate entao

class RecipeSpider(scrapy.Spider):
    name = 'recipes'

    # start_urls = ['https://www.tudogostoso.com.br/categorias/1004-carnes']

    start_urls = [
        'https://www.tudogostoso.com.br/receita/6351-empadao-de-frango.html',
        'https://www.tudogostoso.com.br/receita/302-pizza-de-pao-de-forma.html',
        'https://www.tudogostoso.com.br/receita/760-panqueca-de-carne-moida.html',
        'https://www.tudogostoso.com.br/receita/19817-lasanha-a-bolonhesa.html',
        'https://www.tudogostoso.com.br/receita/309171-macarrao-ao-molho-pesto.html',
    ]


    def parse(self, response):
        for recipe in response.xpath("//div[@class='recipe-page']"):
            loader = ItemLoader(item=TitleItem(), selector=recipe)
            loader.add_xpath('title', "//div[@class='recipe-title']/h1")
            yield {
                'title': loader.get_output_value('title'),
                'link': response.url
            }
