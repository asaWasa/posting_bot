from mongodriver import MongoDriver


class MongoFactory:

    def __init__(self, db_name, collection_name):
        self._db_name = db_name
        self._collection_name = collection_name

    def generate(self):
        return MongoDriver(self._db_name, self._collection_name)
