

class QueueManager:
    def __init__(self, manager_queue):
        self.manager_queue = manager_queue

    def start_manager(self):
        flag = True
        while flag:
            if self.manager_queue.is_empty():
                pass
