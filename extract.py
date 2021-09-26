#%%
import re
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

FILENAME_ALL_DATA = 'data/discours.json'
FILENAME_METADATA = 'data/discours__metadata.json'

# delete file if exists

import os
if os.path.exists(FILENAME_ALL_DATA):
    os.remove(FILENAME_ALL_DATA)

if os.path.exists(FILENAME_METADATA):
    os.remove(FILENAME_METADATA)

START_URL = os.getenv('START_URL')

if START_URL == None or START_URL == "":
    # sets default 
    START_URL = "https://www.vie-publique.fr/discours"

class ViePubliqueSpider(scrapy.Spider):

    name = 'vie_publique'
    allowed_domains = ['vie-publique.fr']
    start_urls = [START_URL]
    link_extractor = LinkExtractor(restrict_css='div .teaserSimple--content')

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES" : {
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
            },
        'FEED_FORMAT': 'json',
        'FEED_URI': FILENAME_ALL_DATA,
        'LOG_LEVEL': 'INFO', 
        'LOG_FORMAT': '%(levelname)s: %(message)s',
        'LOG_FILE':'data/logs-extract.log'#,
        #'CLOSESPIDER_ITEMCOUNT': 50
         # for testing purposes
    }
 

    def parse(self, response):
        # Sur une page, on va chercher les discours référencés
        for link in self.link_extractor.extract_links(response):
            yield Request(link.url, callback=self.parse_speech)
        # crawl de la page suivante
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse)


    def parse_speech(self, response):

        date = response.xpath("//time/@datetime").get()
        self.logger.info("{},{}".format(date,response.url))

        yield {
            "url": response.url,
            "title": response.css("h1::text").get(),
            "raw_text": response.css(".field--name-field-texte-integral").get(),
            "circumstance" : response.css(".field--name-field-circonstance::text").get(),
            "date": date,
            "what_keywords": [tag.strip() for tag in response.css(".btn-tag::text").getall()],
            "desc": response.css(".discour--desc > h2::text").get(),
            "who_keywords": response.css("ul.line-intervenant").css("li::text").getall() + response.css("ul.line-intervenant").css("li").css("a::text").getall(),
        }


from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()                
process.crawl(ViePubliqueSpider)
process.start()

# %%
import pandas as pd

df_discours = pd.read_json(FILENAME_ALL_DATA, orient="records")
# un peu de nettoyage
df_discours["title"] = df_discours["title"].str.strip()
df_discours["who_keywords"] = df_discours.apply(
    lambda row : [item.replace("-\n","").strip() for item in row["who_keywords"]],
    axis = 1
)

df_discours.drop(columns=["raw_text"],inplace=True)
df_discours.to_json(FILENAME_METADATA,orient="records")



