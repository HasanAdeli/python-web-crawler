from abc import ABC, abstractmethod
from urllib.parse import urlparse


class AbstractValidator(ABC):
    def __init__(self, base_url, url):
        self.base_url = base_url
        self.url = url

    @abstractmethod
    def not_valid(self):
        pass


class IsSameDomain(AbstractValidator):
    def __init__(self, base_url, url):
        super().__init__(base_url, url)

    def not_valid(self):
        base_url_domain = urlparse(self.base_url).netloc
        host = base_url_domain
        if base_url_domain.startswith('www.'):
            host = base_url_domain[4:]
        new_url_domain = urlparse(self.url).netloc
        return base_url_domain != new_url_domain and host not in new_url_domain


class IsEmail(AbstractValidator):
    def __init__(self, base_url, url):
        super().__init__(base_url, url)

    def not_valid(self):
        return self.url.startswith('mailto')


class IsPhoneNumber(AbstractValidator):
    def __init__(self, base_url, url):
        super().__init__(base_url, url)

    def not_valid(self):
        return self.url.startswith('tel')


class IsLocal(AbstractValidator):
    def __init__(self, base_url, url):
        super().__init__(base_url, url)

    def not_valid(self):
        return urlparse(self.url).fragment or self.url == '#'


class IsPseudo(AbstractValidator):
    def __init__(self, base_url, url):
        super().__init__(base_url, url)

    def not_valid(self):
        return urlparse(self.url).scheme == 'javascript'


def get_valid_urls(base_url, urls):
    urls['Urls'] = list(set(urls['Urls']))
    urls['Urls'] = [url for url in urls['Urls'] if is_valid_url(base_url, url)]
    return urls


def is_valid_url(base_url: str, url: str) -> bool:
    for sub_class in AbstractValidator.__subclasses__():
        sub = sub_class(base_url, url)
        if sub.not_valid():
            return False
    return True
