from common.constants import INSTAGRAM
from getter.browser_getter import BrowserGetter
from time import sleep
from selenium.webdriver.common.keys import Keys
import datetime


class BrowserInstagram:
    def __init__(self, user_object, browser_getter=None):
        self.login = user_object['login']
        self.password = user_object['password']
        self.browser_getter = browser_getter
        self.getter = self.browser_getter.get_browser()
        self.driver = self.getter.driver
        self.page = None
        self.time = None
        self.location = None

    def __get_page(self, url=None):
        self.page = self.browser_getter.get_page(url)

    def make_post(self, user_queue_object):
        self.__get_page(INSTAGRAM.MAIN_PAGE_BROWSER)
        self.__proc_authorization()
        self.__get_page()
        self.__click_make_post()
        self.__upload_data(user_queue_object)
        self.__commit_post()

    def __proc_authorization(self):
        self.__switch_to_instagram()
        self.__start_auth_instagram()
        self.__authorization()

    def __switch_to_instagram(self):
        self.driver = self.getter.driver
        switch_inst = self.driver.find_element_by_id('media_manager_chrome_bar_instagram_icon')
        switch_inst.click()

    def __start_auth_instagram(self):
        auth_inst = self.driver.find_element_by_class_name('rwb8dzxj')
        auth_inst.click()
        sleep(7)
        self.browser_getter.switch_window(1)
        sleep(2)

    def __authorization(self):
        """input_user_data and authorization in instagram """
        login_input = self.driver.find_element_by_name('username')
        login_input.send_keys(self.login)
        sleep(2)
        pass_input = self.driver.find_element_by_name('password')
        pass_input.send_keys(self.password)
        pass_input.send_keys(Keys.RETURN)
        sleep(4)
        self.__skip_notification()
        self.browser_getter.switch_window(0)
        sleep(5)

    def __click_make_post(self):
        self.driver = self.getter.driver
        make_post = self.driver.find_element_by_class_name('k6xjwoyg')
        make_post.click()
        tape_inst = self.driver.find_element_by_xpath('//*[@id="facebook"]/body/div[3]/div[1]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div/div')
        tape_inst.click()
        sleep(4)

    def __upload_data(self, _object):
        self.__load_image(_object['image'])
        self.__load_caption(_object['caption'])
        self.__set_time(_object['time'])
        self.__set_location(_object['location'])

    def __load_image(self, image):
        btn = self.driver.find_element_by_class_name('_82ht')
        btn.click()
        self.driver.find_element_by_css_selector("input[type=file]").send_keys(image)
        sleep(2)

    def __load_caption(self, caption):
        btn = self.driver.find_element_by_xpath("//*[@aria-autocomplete='list']")
        btn.send_keys(caption)
        sleep(2)

    def __set_time(self, time=10):
        date = dict()
        self.time = time * 60
        self.time = (datetime.datetime.now().timestamp() + self.time) // 1
        date['date'], date['time'] = str(datetime.datetime.fromtimestamp(self.time).strftime("%d.%m.%Y %H:%M")).split()
        date['time'] = date['time'].split(':')
        self.time = date

    def __set_location(self, location):
        self.location = location

    def __skip_notification(self):
        try:
            skip = self.driver.find_element_by_class_name('cmbtv')
            skip.click()
        except Exception as e:
            print(e)
            pass

    def __commit_post(self):
        self.__click_publish()
        self.__switch_scheduled_publish()
        self.__set_date()
        self.__set_hour()
        self.__set_minute()
        self.__submit()

    def __click_publish(self):
        btn = self.driver.find_element_by_xpath("//*[@id='js_3l']")
        btn.click()
        sleep(2)

    def __switch_scheduled_publish(self):
        btn = self.driver.find_element_by_xpath("//*[@class='_811a _811b _811c _3qn7 _61-0 _2fyh _3qnf']")
        btn.click()
        sleep(2)

    def __set_date(self):
        btn = self.driver.find_element_by_css_selector(
            "#js_3m > div > div > div > div > div:nth-child(2) > div > div._811e > div > div:nth-child(2) > div > span > div > span > label > input")
        btn.click()
        sleep(1)
        btn.send_keys(self.time['date'])
        sleep(2)

    def __set_hour(self):
        btn = self.driver.find_element_by_xpath("//*[@class='_4nx7 _4nww _1jg_']/div[@class='_4nwx']/input")
        btn.click()
        btn.send_keys(int(self.time['time'][0]))
        sleep(2)

    def __set_minute(self):
        btn = self.driver.find_element_by_xpath("//*[@class='_4nxe _4nww _1jg_']/div[@class='_4nwx']/input")
        btn.click()
        btn.send_keys(int(self.time['time'][1]))
        sleep(2)

    def __submit(self):
        btn = self.driver.find_element_by_xpath(
            "//*[@id='creator_studio_sliding_tray_root']/div/div/div[3]/div[2]/button")
        btn.click()
        sleep(2)


inst = BrowserInstagram({'login': 'doncov-danil@mail.ru',
                         'password': 'ZEg-5q6-6e7-Acx'}, BrowserGetter())
inst.make_post({'image': '/home/mecing/Desktop/Project/posting_bot/posting_tools/instagram/instagram_browser/1.jpg',
                'caption': 'test',
                'time': 15,
                'location': None})
