import time
from common.errors import *


class Manager:
    def __init__(self, manager_queue):
        self.flag = True
        self.factory = None
        self.handler = None
        self.name_handler = None
        self.manager_queue = manager_queue

    def start(self):
        self.flag = True
        request = dict()
        while self.flag:
            if not self.manager_queue.is_empty():
                try:
                    request = self.manager_queue.pop()
                    self.__check(request)
                    self.__run_request(request)
                except BadRequest:
                    print('Bad request - {}'.format(request))
                except EmptyRequest:
                    print('Empty request')
                except RequestIsNone:
                    print('Request is None')
                except Exception as e:
                    print(e)
            time.sleep(1)

    def __check(self, req):
        self.__check_request(req)
        self.__check_name_handler()

    def __check_request(self, request):
        if not request:
            raise EmptyRequest
        if request is None:
            raise RequestIsNone

    def __check_name_handler(self):
        if self.name_handler is None:
            raise BadNameHandler
        if not self.name_handler:
            raise BadNameHandler

    def __run_request(self, request):
        user_id = self.__get_id_from_request(request)
        data = self.__get_user_data_from_database(user_id)
        social_media_user_data = self.get_social_media_data(data)
        concrete_class = self.handler(social_media_user_data, request)
        concrete_class.start_handler()

    def __get_id_from_request(self, request):
        try:
            return request['user_id']
        except:
            raise BadRequest

    def __get_user_data_from_database(self, user_id) -> dict:
        try:
            user_id = int(user_id)
            # todo исправить, явно неправильно работает
            users_data = self.factory.generate()
            #todo исправить формат базы с пользователями
            return users_data.get('id', user_id)
        except:
            # todo выкинуть наверх ошибку
            print('user_id not find')

    def get_social_media_data(self, data):
        #todo поменять на константу
        social_net = data['social_network']
        return social_net[self.name_handler]
