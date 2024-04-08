import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import os
from googlesearch import search
import spacy
nlp = spacy.load('en_core_web_sm')

article_list = []

class BlogspiderSpider(scrapy.Spider):
    name = "blogspider"
    
    def __init__(self, url):
        self.start_urls = [url]
        self.output_file = f"{self.get_filename(url)}.csv"

    def parse(self, response):
        try:
            texts = response.css('div p ::text').getall()
            if texts:
                content = ' '.join(texts)
                yield {
                    'content': content
                }
            else:
                self.logger.warning(f"No content found on {response.url}")
        except Exception as e:
            self.logger.error(f"Error occurred while parsing {response.url}: {str(e)}")
    
    def get_filename(self, url):
        return f"{url.split('//')[-1].split('/')[0]}.csv"
    
def scrape_urls(urls):
    process = CrawlerProcess(settings={
        "FEEDS": {},
    })
    for url in urls:
        process.settings["FEEDS"][BlogspiderSpider(url).output_file] = {
            "format": "csv"
        }
        process.crawl(BlogspiderSpider, url=url)
        
    process.start()

    for url in urls:
        filename = BlogspiderSpider(url).output_file
        if os.path.isfile(filename) and os.path.getsize(filename) > 0:
            df = pd.read_csv(filename)
            Total_text = ''.join(df['content'])
            article_list.append(Total_text)
            os.remove(filename)

#query = """It's the cow that's looking at the stars.Twice as many stars for having 2 heads to see them with."""
query = """Moore's law is the observation that the number of transistors in an integrated circuit (IC) doubles about every two years."""

num_results = 5

doc = nlp(query)
sentences = [sent.text.strip() for sent in doc.sents]
total_sentences = len(sentences)

urls_dict = {}

for sentence in sentences:
  urls = []
  num_results = 10

  for j in search(sentence, num_results=num_results, advanced=True, sleep_interval=5):
    urls.append(j.url)

  urls_dict[sentence] = urls
  urls = []

urls = [url for url_list in urls_dict.values() for url in url_list]

scrape_urls(urls) 

plag_count = 0   
i = 0 
matched_sentences = set()
matched_urls = set()

for article in article_list:
    for sentence in sentences:
        if sentence in article:
            matched_sentences.add(sentence)
            matched_urls.add(urls[i])
            i=i+1
            break

plag_count = len(matched_sentences)
plag_percentage = (plag_count / total_sentences) * 100
print(f"Plagiarism Percentage = {plag_percentage:.2f}%")

print("URLS FOUND :-")
for val in matched_urls:
    print(val)






