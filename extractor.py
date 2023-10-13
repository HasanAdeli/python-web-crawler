from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class AbstractExtractor(ABC):
    def __init__(self, base_url):
        self.base_url = base_url

    @abstractmethod
    def extract(self, source_code):
        pass


class UrlsExtractor(AbstractExtractor):
    def __init__(self, base_url):
        super().__init__(base_url)

    def extract(self, source_code):
        return [urljoin(self.base_url, tag.get('href')) for tag in source_code.find_all('a') if tag.get('href')]


class CssUrlsExtractor(AbstractExtractor):
    def __init__(self, base_url):
        super().__init__(base_url)

    def extract(self, source_code):
        return [
            urljoin(self.base_url, tag.get('href')) for tag in source_code.find_all('link')
            if tag.get('href') and tag.get('rel')[0] == 'stylesheet'
        ]


class JsUrlsExtractor(AbstractExtractor):
    def __init__(self, base_url):
        super().__init__(base_url)

    def extract(self, source_code):
        return [urljoin(self.base_url, tag.get('src')) for tag in source_code.find_all('script') if tag.get('src')]


class ImgUrlsExtractor(AbstractExtractor):
    def __init__(self, base_url):
        super().__init__(base_url)

    def extract(self, source_code):
        return (
            [urljoin(self.base_url, tag.get('src')) for tag in source_code.find_all('img') if tag.get('src')] +
            [urljoin(self.base_url, tag.get('data-src')) for tag in source_code.find_all('img')if tag.get('data-src')]
        )


class VideoUrlsExtractor(AbstractExtractor):
    def __init__(self, base_url):
        super().__init__(base_url)

    def extract(self, source_code):
        return [urljoin(self.base_url, tag.get('src')) for tag in source_code.find_all('video') if tag.get('src')]


class AudioUrlsExtractor(AbstractExtractor):
    def __init__(self, base_url):
        super().__init__(base_url)

    def extract(self, source_code):
        return [urljoin(self.base_url, tag.get('src')) for tag in source_code.find_all('audio') if tag.get('src')]


def url_extractor(base_url, response):
    all_urls = {'DocUrls': []}
    source_code = BeautifulSoup(response.text, 'html.parser', from_encoding="utf-8")
    for sub_class in AbstractExtractor.__subclasses__():
        extractor = sub_class(base_url)
        extractor_name = sub_class.__name__.replace('Extractor', '')
        all_urls[extractor_name] = extractor.extract(source_code)
    return all_urls
