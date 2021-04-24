from getter.browser import Browser
from bs4 import BeautifulSoup


class BrowserGetter:
    def __init__(self):
        self.browser = Browser(headless=False)

    def get_page(self, page=None):
        try:
            html = self.get_html(page)
            text = BeautifulSoup(html, 'lxml')
            return text
        except Exception as e:
            print(e)

    def get_html(self, page=None):
        return self.browser.get_html(page)

    def restart(self):
        self.browser.restart()

    def free(self):
        self.browser.free()
