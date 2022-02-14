from common.constants import UserRequest, UserTypeRequest
from common.errors import *


class Handler:
    def __init__(self):
        self.handler = None
        self.factory = None
        self.queue_generator = None
        self.request = None
        self.log = None

    def start_handler(self):
        try:
            if self.request[UserRequest.Type_request] == UserTypeRequest.Post_image:
                result = self.handler.make_post(self.request)
                self.__change_user_data(result)
            else:
                self.log('impossible request {}'.format(self.request))
        except NoValidToken:
            pass
        except Exception as e:
            pass

    def __change_user_data(self, result):
        #todo закинуть оставшиеся квоты пользователю в данные
        pass
