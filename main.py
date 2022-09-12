from collection_creation_crawler import CollectionCreationCrawler
import os

if __name__ == '__main__':
    apikey = os.environ['apikey']
    start_block = int(os.environ['start_block'])
    crawler = CollectionCreationCrawler(apikey)
    crawler.run(start_block)
