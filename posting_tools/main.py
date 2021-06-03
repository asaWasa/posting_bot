from database.mongodb.mongodriver import MongoDriver
from common.constants import MongoData, QUEUES
import time
from signal import *
from common.constants import UserRequest
# todo подключить логгирование
# todo переделать принты на логи


class Main:
    def __init__(self, main_queue):
        self.flag = True
        self.main_queue = main_queue
        try:
            self.instagram = MongoDriver(db_name=MongoData.db_queues, collection_name=QUEUES.INSTAGRAM)
            # self.vk = MongoDriver(db_name=MongoData.db_queues, collection_name=Queues.Vk)
            # self.youtube = MongoDriver(db_name=MongoData.db_queues, collection_name=Queues.YouTube)
        except Exception as e:
            print(e)

    def start_main(self):
        try:
            while self.flag:
                try:
                    if not self.main_queue.is_empty():
                        self.__processing_request(self.main_queue.pop())
                except Exception as e:
                    print(e)
                time.sleep(1)
        except Exception as e:
            print(e)

    def __processing_request(self, request):
        try:
            if "instagram" in request[UserRequest.Name]:
                self.instagram.push(request)

        except Exception as e:
            print(e)


def clean(signum, frame):
    main.flag = False


main_queue = MongoDriver(db_name=MongoData.db_main, collection_name=MongoData.db_collection_requests)
# main_queue = MongoDriver(db_name=MongoData.db_queues, collection_name=MongoData.db_collection_main_queue)

main = Main(main_queue)

for sig in (SIGTERM, SIGILL, SIGINT):
    signal(sig, clean)

main.start_main()
