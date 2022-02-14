from common.constants import MongoData


class Stats:
    def __init__(self, factory=None):
        self.db_errors = factory(db_name=MongoData.db_main, collection_name=MongoData.db_collection_errors).generate()
        self.db_users = factory(db_name=MongoData.db_main, collection_name=MongoData.db_collection_user).generate()

    def get_statistic(self):
        try:
            users = self.__get_count_users()
        except: users = 0
        try:
            errors = self.__get_count_errors()
        except: errors = 0

        return users, errors

    def __get_count_errors(self):
        return self.db_errors.get_count()

    def __get_count_users(self):
        return self.db_users.get_count()
