from pymongo import MongoClient


class MongoDriver:

    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        self.__init(self.db_name, self.collection_name)

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

    def get(self, index=None, value=None):
        try:
            result = self.collection.find_one({index: value})
            return result
        except Exception as e:
            print(e)
            pass

    def get_count(self, param='id_request'):
        self.__prepare()
        return self.collection.count()

    def is_empty(self):
        self.__prepare()
        return self.collection.find_one({}) is None

    def update_id(self, index, id_, data):
        try:
            self.__prepare()
            self.collection.update({index: id_}, {'$set': data}, upsert=True)
        except Exception as e:
            print(str(e) + str(2))

    def pop(self, index=None, value=None):
        try:
            self.__prepare()
            if index is None:
                result = self.collection.find_one_and_delete({})
            else:
                result = self.collection.find_one_and_delete({index: value})
            return result
        except Exception as e:
            print(e)

    def if_in(self, index=None, value=None):
        self.__prepare()
        return self.collection.find_one({index: value}) is not None

    def restart(self):
        self.__init(self.db_name, self.collection_name)

    def __prepare(self):
        try:
            self.client.server_info()
        except:
            self.restart()
