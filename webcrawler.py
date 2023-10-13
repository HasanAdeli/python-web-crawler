import requests
from time import sleep
from urllib.parse import urlparse
from extractor import url_extractor
from validator import get_valid_urls
from separator import url_separator


class WebCrawler:
    def __init__(self, url: str, interval: int = 0):
        self.base_url: str = url
        self.urls: list = [url]
        self.interval: int = interval
        self.crawled_url: list = []
        self.css_urls: list = []
        self.js_urls: list = []
        self.img_urls: list = []
        self.video_urls: list = []
        self.audio_urls: list = []
        self.doc_urls: list = []
        self.session = None
        self.set_session()

    def set_session(self):
        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'}
        )

    def send_request(self, url: str):
        print(f'A request was sent to the: {url[:50]}')
        response = self.session.get(url)
        print(f'Response status code: {response.status_code}')
        return response

    @staticmethod
    def extract_all_urls(base_url: str, response: requests) -> dict:
        return url_extractor(base_url, response)

    @staticmethod
    def get_valid_urls(base_url: str, urls: dict) -> dict:
        return get_valid_urls(base_url, urls)

    @staticmethod
    def separate_urls(urls: dict) -> dict:
        return url_separator(urls)

    def save_all_urls(self, urls: dict) -> None:
        self.save_urls(self.urls, urls['Urls'])
        self.save_urls(self.css_urls, urls['CssUrls'], 'css')
        self.save_urls(self.js_urls, urls['JsUrls'], 'java script')
        self.save_urls(self.img_urls, urls['ImgUrls'], 'image')
        self.save_urls(self.video_urls, urls['VideoUrls'], 'video')
        self.save_urls(self.audio_urls, urls['AudioUrls'], 'audio')
        self.save_urls(self.doc_urls, urls['DocUrls'], 'document')

    @staticmethod
    def save_urls(old_urls: list, new_urls: list, type_: str = '') -> None:
        for url in new_urls:
            if url not in old_urls:
                old_urls.append(url)
                print(f'A new {type_} url added. [{url}]')

    def start(self):
        print(f'crawling for "{urlparse(self.urls[0]).netloc}" started ...')
        for url in self.urls:
            response = self.send_request(url)
            if response.status_code != 200:
                self.crawled_url.append(url)
                continue

            urls = self.extract_all_urls(self.base_url, response)
            urls = self.get_valid_urls(self.base_url, urls)
            urls = self.separate_urls(urls)
            self.save_all_urls(urls)
            self.crawled_url.append(url)
            print('-' * 200)
            sleep(self.interval)
