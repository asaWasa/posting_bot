from selenium import webdriver


class Browser:

    def __init__(self, headless=False):

        self.driver = None
        self.type = type
        self.headless = headless

        self.init(self.headless)

    def init(self, headless=False):
        option = webdriver.ChromeOptions()
        #
        chrome_prefs = dict()
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        option.experimental_options["prefs"] = chrome_prefs

        option.add_argument('--disable-extensions')
        option.add_argument('--no-sandbox')
        option.add_argument('--incognito')
        option.add_argument('--disable-application-cache')
        option.add_argument('disable-infobars')

        if headless:
            option.add_argument('--headless')

        self.driver = webdriver.Chrome(chrome_options=option)

    def get_html(self, url=None):
        if url and url is not None:
            self.driver.get(url)
            return self.driver.page_source
        else:
            return self.driver.page_source

    def get_page(self, url):
        self.driver.get(url)
        return self.driver

    def free(self):
        try:
            if self.driver is not None:
                self.driver.quit()
                self.driver.close()
                self.driver = None
        except Exception as e:
            print(e)

    def restart(self):
        self.free()
        self.init(self.headless)

    def switch_window(self, n_window):
        self.driver.switch_to.window(self.driver.window_handles[n_window])
