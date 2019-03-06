from scrapy.spiders import CrawlSpider, Rule,Request
from scrapy.linkextractors import LinkExtractor
from helpers import *
class LarousseCrawler(CrawlSpider):
    name = 'laroussecrawler'
    start_urls = ['https://www.larousse.fr/dictionnaires/francais/femme/33217?q=femme#33141']
    allowed_domains = ['larousse.fr']
    rules = (
        Rule(LinkExtractor(allow=[
             r'dictionnaires\/francais\/[A-Za-z0-9]+\/[0-9]+(.+)?$']), callback='parse_page', follow=True),
    )
    custom_settings = {
        'LOG_ENABLED': False,
        'ROBOTSTXT_OBEY':False
    }
    iteration = 0
    total = 0
    def parse_page(self,response):
        try:
            audio_link_native = response.css('a.lienson').xpath('@href').get()
            word = response.css('.AdresseDefinition').xpath('text()').get()
            if word and audio_link_native:
                word = word.lower().strip()
                audio_link = "https://www.larousse.fr"+audio_link_native
                path = "data/audio/"+word
                if not folder_exist(path):
                    self.total+=1
                    printProgressBar(self.iteration, self.total,str(self.iteration)+'/'+str(self.total))
                    yield Request(audio_link, self.parse_link,meta={'word':word})
        except Exception as e:
            print(str(e))

    def parse_link(self,response):
        audio_name = response.meta['word']+".mp3"
        path = "data/audio/"+response.meta['word']
        if create_dir(path):
            self.iteration += 1
            
            with open("data/audio/"+response.meta['word']+"/"+audio_name, 'wb') as f:
                f.write(response.body)
            with open("data/wordlist.txt", 'a') as wls:
                wls.write(response.meta['word']+'\n')

