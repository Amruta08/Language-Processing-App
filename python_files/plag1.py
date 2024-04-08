import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import os
from googlesearch import search
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
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
    print(len(article_list))

query = "Today is the anniversary of the publication of Robert Frost's iconic poem “Stopping by Woods on a Snowy Evening,” a fact that spurred the Literary Hub office into a long conversation about their favorite poems, the most iconic poems written in English, and which poems we should all have already read (or at least be reading next)."

# Code starts from here :-
num_results = 10

doc = nlp(query)
sentences = [sent.text.strip() for sent in doc.sents]
total_sentences = len(sentences)

urls_dict = {}

for sentence in sentences:
  urls = []
  num_results = 5

  for j in search(sentence, num_results=num_results, advanced=True, sleep_interval=5):
    urls.append(j.url)

  urls_dict[sentence] = urls
  urls = []

urls = [url for url_list in urls_dict.values() for url in url_list]

scrape_urls(urls) 

plag_count = 0

def preprocess(text):
    # Tokenization, lowercase conversion, and punctuation removal (add stop word removal if needed)
    return [word.lower() for word in text.split()]

# Compute sentence vectors
def sentence_vector(tokens):
    vectors = [word2vec_model.wv[word] for word in tokens if word in word2vec_model.wv]
    return np.mean(vectors, axis=0) if vectors else np.zeros(word2vec_model.vector_size)

# Initialize a set to store sentences that have been matched
matched_sentences = set()

for article in article_list:
  paragraph_tokens = [preprocess(sentence) for sentence in article.split(".")]

  # Word embedding model (example using Word2Vec)
  word2vec_model = Word2Vec(paragraph_tokens, vector_size=100, window=5, min_count=1, sg=1)
  paragraph_vectors = [sentence_vector(tokens) for tokens in paragraph_tokens]

  for sentence in sentences:
    #print(sentence)
    input_tokens = preprocess(sentence)
    input_vector = sentence_vector(input_tokens)

    # Compute cosine similarity
    similarities = [cosine_similarity([input_vector], [sentence_vector])[0][0] for sentence_vector in paragraph_vectors]

    threshold = 0

    # Check if input sentence exists in the paragraph
    exists = any(similarity > threshold for similarity in similarities)
    print("Sentence exists in paragraph:", exists)

    if exists:
      matched_sentences.add(sentence)

    # Cosine similarity of input sentence with sentences in the paragraph
    for i, similarity in enumerate(similarities):
        print(f"Sentence {i+1}: Cosine Similarity = {similarity:.2f}")


plag_count = len(matched_sentences)
plag_percentage = (plag_count / total_sentences) * 100

print(f"Plagarism Percentage = {(plag_count/total_sentences)*100:.2f}%")
 






