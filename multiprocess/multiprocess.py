from multiprocessing import Process


class Multiprocess:
    def __init__(self, handler, factory, request, user_data):
        self.handler = handler
        self.factory = factory
        self.request = request
        self.user_data = user_data

    def start(self):
        classes = list()
        list_process = list()
        concrete_class = self.handler(self.user_data, self.request)
        process_object = Process(target=concrete_class.start_handler, args=tuple())
        process_object.start()
        list_process.append(process_object)
        classes.append(concrete_class)
        for process in list_process:
            process.join()
        for process in list_process:
            process.terminate()
        classes.clear()
