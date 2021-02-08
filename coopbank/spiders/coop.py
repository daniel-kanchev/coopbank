import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from coopbank.items import Article


class CoopSpider(scrapy.Spider):
    name = 'coop'
    start_urls = ['https://www.co-operativebank.co.uk/news']

    def parse(self, response):
        head_link = response.xpath('//p[@class="u-text-right"]/a/@href').get()
        print(head_link)
        yield response.follow(head_link, self.parse_article)

        links = response.xpath('//a[@class="link-secret"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        print('xd')
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('(//h2)[1]/text()').get().strip()
        date = response.xpath('//p[@class="u-mb+"]/text()').get().strip()
        date = datetime.strptime(date, '%d %B %Y')
        date = date.strftime('%Y/%m/%d')
        content = response.xpath('//div[@class="c-pr-local-nav-content-area u-p o-layout__item u-3/4@md"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)
        # item.add_value('author', author)
        # item.add_value('category', category)
        # item.add_value('tags', tags)

        return item.load_item()

# response.xpath('').get()

