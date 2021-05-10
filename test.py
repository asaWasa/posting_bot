import json
from posting_tools.tmp_photo import photo_path
from database.mongodb.MongoFactory import MongoFactory
from common.constants import *
import datetime
import requests

db = MongoFactory(db_name=MongoData.db_main, collection_name=MongoData.db_collection_requests)
users_requests = db.generate()

db = MongoFactory(db_name=MongoData.db_main, collection_name=MongoData.db_collection_invite)
users_invite = db.generate()


def get_id():

    return users_requests.get_last_item('id_request')['id_request']


# _id = get_id()+1

# users_requests.push(
#     {'id_request': _id,
#      'user_id': '12345677',
#      'type_request': 'POST_IMAGE',
#      'data': {'image': 'https//...',
#               'caption': 'text',
#               'delay': 10},
#      'date_creation': datetime.datetime.now()})

# print(photo_path.get_filepath())
users_invite.push({
    Invite.Invite_key: 'test'
})

def __api_call(self, url, endpoint_data, type):
    if type == RequestType.POST:
        data = requests.post(url, endpoint_data)
    else:
        data = requests.get(url, endpoint_data)

    response = dict()
    response['url'] = url
    response['endpoint_params'] = endpoint_data
    response['endpoint_params_pretty'] = json.dumps(endpoint_data)
    response['json_data'] = json.loads(data.content)
    response['json_data_pretty'] = json.dumps(response['json_data'])
    return response
