from database.mongodb.mongodriver import MongoDriver
from common.constants import MongoData, Queues
import time
from signal import *
from database.mongodb.MongoFactory import MongoFactory


class Manager:
    def __init__(self, manager_queue):
        self.flag = True
        self.manager_queue = manager_queue
        try:
            self.instagram = MongoDriver(db_name=MongoData.db_queues, collection_name=Queues.Instagram)
            # self.vk = MongoDriver(db_name=MongoData.db_queues, collection_name=Queues.Vk)
            # self.youtube = MongoDriver(db_name=MongoData.db_queues, collection_name=Queues.YouTube)
        except Exception as e:
            print(e)

    def start_manager(self):
        try:
            while self.flag:
                try:
                    if not self.manager_queue.is_empty():
                        self.__processing_request(self.manager_queue.pop())
                except Exception as e:
                    print(e)
                time.sleep(1)
        except Exception as e:
            print(e)

    def __processing_request(self, request):
        try:
            if "instagram" in request:
                self.instagram.push(request)

        except Exception as e:
            print(e)


def clean(signum, frame):
    manager.flag = False


main_queue = MongoFactory(db_name=MongoData.db_queues, collection_name=MongoData.db_collection_main_queue)
# main_queue = MongoDriver(db_name=MongoData.db_queues, collection_name=MongoData.db_collection_main_queue)

manager = Manager(main_queue)

for sig in (SIGTERM, SIGILL, SIGINT):
    signal(sig, clean)

manager.start_manager()
