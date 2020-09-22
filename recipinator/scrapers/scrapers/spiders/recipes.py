import scrapy
from scrapers.items import RecipeItem
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
        # works (: now I just need to learn how to deal with the list.)
        for recipe in response.xpath("//div[@class='recipe-page']"):
            loader = ItemLoader(item=RecipeItem(), selector=recipe)
            loader.add_xpath('title', "//div[@class='recipe-title']/h1")
            loader.add_xpath('ingredient_list', ".//li/span[@class='p-ingredient']")
            yield loader.load_item()            
            # yield {
            #     'title': recipe.xpath("//div[@class='recipe-title']/h1").extract_first(),
            #     'ingredient_list': ingredient_list.extract()
            # }

        # next_page = response.xpath("//li[@class='next']/a/@href").extract_first()

        # if next_page is not None:
        #     next_page_link = response.urljoin(next_page)
        #     yield scrapy.Request(url=next_page_link, callback=self.parse)
