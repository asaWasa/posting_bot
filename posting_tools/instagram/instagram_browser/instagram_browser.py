from common.constants import INSTAGRAM
import selenium


class BrowserInstagram:
    def __init__(self, user_object, getter=None):
        self.login = user_object['login']
        self.password = user_object['password']
        self.getter = getter
        self.page = None

    def __get_page(self, url=None):
        self.page = self.getter.get_page(url)

    def make_post(self, user_queue_object):
        self.__get_page(INSTAGRAM.MAIN_PAGE_BROWSER)
        self.__proc_auth()
        self.__get_page()
        self.__click_make_post()
        self.__load_data(user_queue_object)

    def __proc_auth(self):
        pass

    def __click_make_post(self):
        pass

    def __load_data(self, _object):
        self.__load_image(_object['image'])
        self.__load_caption(_object['caption'])
        self.__set_time(_object['time'])
        self.__set_location(_object['location'])

    def __load_image(self, param):
        pass

    def __load_caption(self, param):
        pass

    def __set_time(self, param):
        pass

    def __set_location(self, param):
        pass
