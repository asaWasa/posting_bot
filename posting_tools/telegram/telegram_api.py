import requests
from common.config import api_key
from common.constants import Key
from json import loads


def get_file_path(file_id):
    r = requests.get("https://api.telegram.org/bot{}/getFile?file_id={}".format(api_key[Key.Api], file_id))
    return loads(r.content)['result']['file_path']


def get_photo_path(file_id):
    path = get_file_path(file_id)
    return "https://api.telegram.org/file/bot{}/{}".format(api_key[Key.Api], path)


