from common.constants import INSTAGRAM
from getter.browser_getter import BrowserGetter
from time import sleep
from selenium.webdriver.common.keys import Keys


class BrowserInstagram:
    def __init__(self, user_object, browser_getter=None):
        self.login = user_object['login']
        self.password = user_object['password']
        self.browser_getter = browser_getter
        self.getter = self.browser_getter.get_browser()
        self.page = None
        self.driver = self.getter.driver

    def __get_page(self, url=None):
        self.page = self.browser_getter.get_page(url)

    def make_post(self, user_queue_object):
        self.__get_page(INSTAGRAM.MAIN_PAGE_BROWSER)
        self.__proc_auth()
        self.__get_page()
        self.__click_make_post()
        self.__upload_data(user_queue_object)
        self.__commit_post()

    def __proc_auth(self):
        """
        authorization to instagram
        """
        self.driver = self.getter.driver
        switch_inst = self.driver.find_element_by_id('media_manager_chrome_bar_instagram_icon')
        switch_inst.click()

        """start authorize"""
        auth_inst = self.driver.find_element_by_class_name('rwb8dzxj')
        auth_inst.click()

        sleep(7)
        self.browser_getter.switch_window(1)
        sleep(2)

        """input_user_data"""
        login_input = self.driver.find_element_by_name('username')
        login_input.send_keys(self.login)
        sleep(2)
        pass_input = self.driver.find_element_by_name('password')
        pass_input.send_keys(self.password)
        pass_input.send_keys(Keys.RETURN)
        sleep(4)
        self.__skip_notif()
        self.browser_getter.switch_window(0)
        sleep(4)

    def __click_make_post(self):
        self.driver = self.getter.driver
        make_post = self.driver.find_element_by_class_name('k6xjwoyg')
        make_post.click()
        tape_inst = self.driver.find_element_by_id('js_2r')
        tape_inst.click()
        sleep(2)

    def __upload_data(self, _object):
        self.__load_image(_object['image'])
        self.__load_caption(_object['caption'])
        self.__set_time(_object['time'])
        self.__set_location(_object['location'])

    def __load_image(self, image):
        btn = self.driver.find_element_by_class_name('_3qn7 _61-0 _2fyi _3qng')
        btn.click()
        self.driver.find_element_by_css_selector("input[type=file]").send_keys(image)
        sleep(2)

    def __load_caption(self, caption):
        btn = self.driver.find_element_by_id('placeholder-c0udr')
        btn.send_keys(caption)
        sleep(2)

    def __set_time(self, time):
        pass

    def __set_location(self, location):
        pass

    def __skip_notif(self):
        try:
            skip = self.driver.find_element_by_class_name('cmbtv')
            skip.click()
        except Exception as e:
            print(e)
            pass

    def __commit_post(self):
        pass


inst = BrowserInstagram({'login': 'doncov-danil@mail.ru', 'password': 'iKtKjxqaQ2GJu7t'}, BrowserGetter())
inst.make_post({'image': '1.jpg', 'caption': 'test', 'time': None, 'location': None})
