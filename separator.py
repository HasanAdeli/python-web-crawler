from urllib.parse import urlparse


IMAGE_EXTENSION = ('jpg', 'png', 'apng', 'gif', 'ico', 'svg', 'jpeg', 'webp', 'avi', 'avif', 'bmp')
VIDEO_EXTENSION = ('mp4', 'ogg', 'webm')
AUDIO_EXTENSION = ('mp3', 'ogg', 'wav', 'aif', 'wma', 'wpl')
DOCUMENT_EXTENSION = ('pdf', 'json', 'xml', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'csv', 'tex')
COMPRESSED_FILE_EXTENSIONS = ('zip', 'rar', 'pkg')


class ExtensionIdentifier:

    @staticmethod
    def is_css_url(extension: str) -> bool:
        return extension == 'css'

    @staticmethod
    def is_js_url(extension: str) -> bool:
        return extension == 'js'

    @staticmethod
    def is_img_url(extension: str) -> bool:
        return extension in IMAGE_EXTENSION

    @staticmethod
    def is_video_url(extension: str) -> bool:
        return extension in VIDEO_EXTENSION

    @staticmethod
    def is_audio_url(extension: str) -> bool:
        return extension in AUDIO_EXTENSION

    @staticmethod
    def is_doc_url(extension: str) -> bool:
        return extension in DOCUMENT_EXTENSION

    @staticmethod
    def is_compressed_url(extension: str) -> bool:
        return extension in COMPRESSED_FILE_EXTENSIONS


def url_separator(urls: dict) -> dict:
    for url in urls['Urls']:
        identifier = ExtensionIdentifier()
        extension = get_extension(url)
        if not extension:
            continue

        if identifier.is_css_url(extension):
            move_url(url, urls['Urls'], urls['CssUrls'])

        elif identifier.is_js_url(extension):
            move_url(url, urls['Urls'], urls['JsUrls'])

        elif identifier.is_img_url(extension):
            move_url(url, urls['Urls'], urls['ImgUrls'])

        elif identifier.is_video_url(extension):
            move_url(url, urls['Urls'], urls['VideoUrls'])

        elif identifier.is_audio_url(extension):
            move_url(url, urls['Urls'], urls['AudioUrls'])

        elif identifier.is_doc_url(extension):
            move_url(url, urls['Urls'], urls['DocUrls'])

    return urls


def get_extension(url: str) -> str:
    extension = urlparse(url).path
    if '.' not in extension:
        return ''
    return extension.split('.')[-1].lower()


def move_url(url: str, from_list: list, to_list: list) -> None:
    from_list.remove(url)
    to_list.append(url)
