from posting_tools.handler import Handler
from posting_tools.instagram.instagfram_api.instagram_api import InstagramApi


class InstagramHandler(Handler):
    def __init__(self, user_data, request):
        super().__init__()
        self.factory = None
        self.queue_generator = None
        self.user_data = user_data
        self.request = request

        self.handler = InstagramApi(self.user_data)
