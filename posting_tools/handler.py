from common.constants import UserRequest, UserTypeRequest


class Handler:
    def __init__(self):
        self.handler = None
        self.factory = None
        self.queue_generator = None
        self.request = None

    def start_handler(self):
        # todo требуется обработка ошибок
        if self.request[UserRequest.Type_request] == UserTypeRequest.Post_image:
            self.handler.make_post(self.request)

        else:
            print('impossible request')
