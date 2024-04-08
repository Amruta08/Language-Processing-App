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
        'LOG_ENABLED': False
    })
    for url in urls:
        process.settings["FEEDS"][BlogspiderSpider(url).output_file] = {
            "format": "csv"
        }
        process.crawl(BlogspiderSpider, url=url)
    process.start()

def plagarism(prompt):
    query = prompt
    num_results = 1
    return_list = []

    doc = nlp(query)
    sentences = [sent.text.strip() for sent in doc.sents]
    total_sentences = len(sentences)
    
    urls_dict = {}
    
    for sentence in sentences:
        urls = []

        for j in search(sentence, num_results=num_results, pause=2):
            urls.append(j)

        urls_dict[sentence] = urls

    urls = [url for url_list in urls_dict.values() for url in url_list]
    scrape_urls(urls)
    
    for url in urls:
        filename = BlogspiderSpider(url).output_file
        if os.path.isfile(filename) and os.path.getsize(filename) > 0:
            df = pd.read_csv(filename)
            Total_text = ''.join(df['content'])
            article_list.append(Total_text)
            os.remove(filename)

    plag_count = 0   
    matched_sentences = set()
    matched_urls = set()

    for article in article_list:
        for sentence in sentences:
            if sentence in article:
                matched_sentences.add(sentence)
                break

    plag_count = len(matched_sentences)
    plag_percentage = (plag_count / total_sentences) * 100
    final_result = f"Plagiarism Percentage = {plag_percentage:.2f}%"
    return_list.append(final_result)

    return_list.append("URLS FOUND :-")
    for val in urls:
        return_list.append(val)
    
    return return_list

new_list = plagarism("This law explains how the number of transistors on integrated circuits is increasing exponentially, which boosts computing capability and lowers prices. More law is all abt phy.")
print(new_list)
