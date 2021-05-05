
from posting_tools.tmp_photo import photo_path
from database.mongodb.MongoFactory import MongoFactory
from common.constants import *
import datetime


db = MongoFactory(db_name=MongoData.db_main, collection_name=MongoData.db_collection_requests)
users_requests = db.generate()


def get_id():

    return users_requests.get_last_item('id_request')['id_request']


_id = get_id()+1

users_requests.push({'id_request': _id,
                    'user_id': '12345677',
                    'type_request': 'POST_IMAGE',
                    'data': {'image': 'https//...',
                             'caption': 'text',
                             'delay': 10},
                    'date_creation': datetime.datetime.now()})

# print(photo_path.get_filepath())
