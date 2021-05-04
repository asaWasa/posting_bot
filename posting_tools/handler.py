
class Handler:
    def __init__(self):
        self.handler = None
        self.factory = None
        self.queue_generator = None
        self.request = None

    def start_handler(self):
        if self.request['POST_IMAGE']:
            self.handler.make_post(self.request)
        else:
            print('impossible request')



