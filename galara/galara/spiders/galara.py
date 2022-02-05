
import scrapy
import logging


logger = logging.getLogger('Galaralogs')


class GaSpider(scrapy.Spider):

    name = 'Galara'
    start_urls = ['https://galara.ru']

    def parse(self, response, **kwargs):

        brands = response.css('div.alpha-block a::attr(href)').getall()
        yield from response.follow_all(brands, callback=self.parse)

        pagination_links = response.css('table.brands a::attr(href)').getall()
        yield from response.follow_all(pagination_links, callback=self.parse)

        pagination_links2 = response.css('div.name a::attr(href)').getall()
        yield from response.follow_all(pagination_links2, callback=self.parse_product)

    def parse_product(self, response):
        def extract_with_css(query):
            return response.css(query).get().strip()

        yield {
            'Наименование продукта': extract_with_css('div.lo img::attr(alt)'),
            'description_table': extract_with_css('.name::text'),
            'description_table_values': extract_with_css('.items::text'),
            'Наименование продукции': extract_with_css('td.n::text'),
            'Объём': extract_with_css('td.v::text'),
            'В наличии': extract_with_css('td.a span::text')
        }