

class ApiInstagram:
    def __init__(self, user_object, user_queue_object, getter=None):
        self.login = user_object['login']
        self.password = user_object['password']
        self.queue_object = user_queue_object
        self.getter = getter

    def __get_page(self, url):
        return self.getter.get_page(url)

    def make_post(self, image, caption):
        page = self.__get_page('https://business.facebook.com/creatorstudio/home')
        self.__proc_auth(page)

    def __proc_auth(self, page):
        pass
