import time
from common.errors import *


class Manager:
    def __init__(self, manager_queue):
        self.flag = True
        self.factory = None
        self.handler = None
        self.manager_queue = manager_queue

    def start(self):
        self.flag = True
        request = dict()
        while self.flag:
            if not self.manager_queue.is_empty():
                try:
                    request = self.manager_queue.pop()
                    self.__check_request(request)
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

    def __check_request(self, request):
        if not request:
            raise EmptyRequest
        if request is None:
            raise RequestIsNone

    def __run_request(self, request):
        user_id = self.__get_id_from_request(request)
        users_data = self.__get_user_data_from_database(user_id)
        concrete_class = self.handler(users_data, request)
        concrete_class.start_handler()

    def __get_id_from_request(self, request):
        try:
            return request['id']
        except:
            raise BadRequest

    def __get_user_data_from_database(self, user_id):
        try:
            users_data = self.factory.generete()
            return users_data.get('id', user_id)
        except:
            print('user_id not find')

    # def __build_multiprocess(self, request, user_data):
    #     multiprocess = Multiprocess(request=request,
    #                                 user_data=user_data,
    #                                 factory=self.factory,
    #                                 handler=self.handler)
    #     return multiprocess
