import requests
import json
from bs4 import BeautifulSoup
from typing import Dict
from utils.singleton import Singleton
import os

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
features = "html.parser"

class Client(metaclass=Singleton):
    
    cache_dir: str = "./cache/"
    cache_results: bool
    scraped: Dict[str, str] = {}

    def __init__(self, cache_results: bool = False):
        self.cache_results = cache_results


    def fetch_cache(self, url: str) -> str:
        filename = self.cache_dir + url

        if not os.path.isfile(filename):
            html_page: str = requests.get(url, headers=headers).text
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as file:
                file.write(html_page)

        if url not in self.scraped:
            with open(filename, "r") as file:
                self.scraped[url] = file.read()

        return self.scraped[url]

    def scrape(self, url: str) -> 'BeautifulSoup':
        
        res = self.fetch_cache(url)
        return BeautifulSoup(res, features=features)


    def fetch(self, url: str):
        
        res = self.fetch_cache(url)
        return json.loads(res)