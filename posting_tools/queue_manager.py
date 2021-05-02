

class QueueManager:
    def __init__(self, manager_queue):
        self.manager_queue = manager_queue

    def start_manager(self):
        try:
            flag = True
            while flag:
                if not self.manager_queue.is_empty():
                    self.__processing_request(self.manager_queue.pop())
        except Exception as e:
            print(e)

    def __processing_request(self, request):
        pass
