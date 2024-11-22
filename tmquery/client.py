import requests
import json
import os
from bs4 import BeautifulSoup
from tmquery.utils.singleton import Singleton

base_url = "https://www.transfermarkt.com"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
features = "html.parser"


class Client(metaclass=Singleton):
    
    cache_results: bool
    cache_dir: str

    def __init__(self, cache_results: bool = False, cache_dir: str = "./cache/"):
        self.cache_results = cache_results
        self.cache_dir = cache_dir


    def fetch_cache(self, url: str) -> str:
        filename = self.cache_dir + url[1:].replace("/", "__")
        data = ""

        if self.cache_results:
            if not os.path.isfile(filename):
                html_page: str = requests.get(base_url + url, headers=headers).text
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, "w") as file:
                    file.write(html_page)

            with open(filename, "r") as file:
                data = file.read()
        else:
            data = requests.get(base_url + url, headers=headers).text
        
        return data
    

    def scrape(self, url: str) -> 'BeautifulSoup':
        
        res = self.fetch_cache(url)
        return BeautifulSoup(res, features=features)


    def fetch(self, url: str):
        
        res = self.fetch_cache(url)
        return json.loads(res)