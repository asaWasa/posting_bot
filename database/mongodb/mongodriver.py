from pymongo import MongoClient


class MongoDriver:

    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name

    def __init(self, db_name, collection_name):
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def push(self, data=None):
        try:
            self.__prepare()
            self.collection.insert_one(data)
        except Exception as e:
            print(e)

    def pop(self, index=None, value=None):
        try:
            self.__prepare()
            if index is None:
                result = self.collection.find_one_and_delete({})
            else:
                result = self.collection.find_one_and_delete({index: value})
            return result
        except:
            pass

    def is_in(self, index=None, value=None):
        self.__prepare()
        return self.collection.find_one({index: value}) is not None

    def is_empty(self):
        self.__prepare()
        return self.collection.find_one({}) is None

    def restart(self):
        self.__init(self.db_name, self.collection_name)

    def find(self, request):
        self.__prepare()
        return self.collection.find(request, no_cursor_timeout=True)

    def __prepare(self):
        try:
            self.client.server_info()
        except:
            self.restart()
