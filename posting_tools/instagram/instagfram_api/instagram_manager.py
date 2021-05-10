from signal import signal as signall
from posting_tools.manager import Manager
from signal import SIGILL, SIGINT, SIGTERM
from common.constants import MongoData, Queues
from database.mongodb.mongodriver import MongoDriver
from database.mongodb.MongoFactory import MongoFactory
from posting_tools.instagram.instagfram_api.Instagram_handler import InstagramHandler


class ManagerInstagram(Manager):

    def __init__(self, manager_queue):
        super().__init__(manager_queue)
        self.manager_queue = manager_queue
        self.handler = InstagramHandler
        self.factory = MongoFactory(db_name=MongoData.db_main, collection_name=MongoData.db_collection_user)


def clean(signum, frame):
    manager.flag = False


queue = MongoFactory(db_name=MongoData.db_queues, collection_name=Queues.Instagram)
users_data = MongoDriver
manager = ManagerInstagram(manager_queue=queue)

for sig in (SIGTERM, SIGILL, SIGINT):
    signall(sig, clean)

manager.start()
