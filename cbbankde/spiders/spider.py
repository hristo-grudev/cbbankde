import scrapy

from scrapy.loader import ItemLoader

from ..items import CbbankdeItem
from itemloaders.processors import TakeFirst


class CbbankdeSpider(scrapy.Spider):
	name = 'cbbankde'
	start_urls = ['https://www.cb-bank.de/firmenprofil/aktuelles/']

	def parse(self, response):
		post_links = response.xpath('//h3[@itemprop="headline"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="last next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@itemprop="articleBody"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=CbbankdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
