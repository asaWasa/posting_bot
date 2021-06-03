from posting_tools.handler import Handler
from posting_tools.instagram.instagram_api.instagram_api import InstagramApi
from self_logging.logger import Log


class InstagramHandler(Handler):
    def __init__(self, user_data, request):
        super().__init__()
        self.factory = None
        self.queue_generator = None
        self.user_data = user_data
        self.request = request
        self.log = Log(logger_name='posting_bot',
                       program_path=__file__,
                       file_name='instagram_api',
                       level='INFO')
        self.handler = InstagramApi(self.user_data, self.log)
