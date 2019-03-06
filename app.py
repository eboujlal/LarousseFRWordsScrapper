# Import Scrapy 
from scrapy.spiders import CrawlSpider, Rule,Request
from scrapy.linkextractors import LinkExtractor
#Import some function helpers
from helpers import * 
class LarousseCrawler(CrawlSpider):
    # Crawler name
    name = 'laroussecrawler'
    # Link where the spiders gonna start
    start_urls = ['https://www.larousse.fr/dictionnaires/francais/femme/33217?q=femme#33141']
    #Domains that the spiders must respect
    allowed_domains = ['larousse.fr']
    # The links that are similar to the start link must be parsed by parse_page function. 
    rules = (
        Rule(LinkExtractor(allow=[
             r'dictionnaires\/francais\/[A-Za-z0-9]+\/[0-9]+(.+)?$']), callback='parse_page', follow=True),
    )
    custom_settings = {
        'LOG_ENABLED': False, # Disable log
        'ROBOTSTXT_OBEY':False # Don't obey the robots.txt
    }
    iteration = 0 # Number of crawled pages
    total = 0 # Number of downloaded audios
    def parse_page(self,response):
        try:
            # get link of the audio pro
            audio_link_native = response.css('a.lienson').xpath('@href').get()
            # get link of the word
            word = response.css('.AdresseDefinition').xpath('text()').get()
            # if the page contains the word and the work pronunciation link then ok
            if word and audio_link_native:
                # transform word to lower and remove extra spcaces
                word = word.lower().strip()
                # audio link don't contains all the url so we need to complete the link
                audio_link = "https://www.larousse.fr"+audio_link_native
                # define the path where to save the audio
                path = "data/audio/"+word
                # if the folder is not exist yet 
                if not folder_exist(path):
                    # total page count, words must be crawled
                    self.total+=1
                    
                    printProgressBar(self.iteration, self.total,str(self.iteration)+'/'+str(self.total))
                    # add link of pronunciation audio to the queue of scrapy and specify the function that will parse this link
                    yield Request(audio_link, self.parse_link,meta={'word':word})
        except Exception as e:
            print(str(e))

    def parse_link(self,response):
        audio_name = response.meta['word']+".mp3"
        path = "data/audio/"+response.meta['word']
        # create the folder if it dosn't exists
        if create_dir(path):
            # number of words that are crawled.
            self.iteration += 1
            # Save the audio of the pronunciation
            with open("data/audio/"+response.meta['word']+"/"+audio_name, 'wb') as f:
                f.write(response.body)

            # Add the word into a wordlist
            with open("data/wordlist.txt", 'a') as wls:
                wls.write(response.meta['word']+'\n')

