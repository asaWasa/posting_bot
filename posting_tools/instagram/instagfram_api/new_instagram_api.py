from time import sleep
import requests
import json


class RequestType:
    POST = 'POST'
    GET = 'GET'


class InstagramApi:
    def __init__(self, user_object):
        self.params = self.__get_user_param(user_object)

    def __get_user_param(self, user_object):
        user_data = self.__get_user_data(user_object)
        user_param = dict()
        # todo заменить инфой из базы
        user_param['access_token'] = user_data['access_token']
        user_param['endpoint_base'] = 'https://graph.facebook.com/v10.0/'
        user_param['instagram_account_id'] = user_data['instagram_account_id']  # todo заменить инфой из базы
        return user_param

    def __api_call(self, url, endpoint_data, type):
        if type == RequestType.POST:
            data = requests.post(url, endpoint_data)
        else:
            data = requests.get(url, endpoint_data)

        response = dict()
        response['url'] = url
        response['endpoint_params'] = endpoint_data
        response['endpoint_params_pretty'] = json.dumps(endpoint_data, indent=4)
        response['json_data'] = json.loads(data.content)
        response['json_data_pretty'] = json.dumps(response['json_data'], indent=4)
        return response

    def __get_user_data(self, user_object):
        """получить данные пользователя из базы данных и выдать"""
        #todo поправить
        user_data = dict()
        user_data['access_token'] = user_object['access_token']
        user_data['instagram_account_id'] = user_object['instagram_account_id']
        return user_data

    def make_post(self, user_request, delay=5):
        """создать медиа объект"""
        media_response = self.__create_media(user_request['image'], user_request['caption'])
        media_id = media_response['data']['json_data']
        while media_response['status'] != 'FINISHED':
            status_media_object = self.get_status_media_object(media_id)
            media_response['status'] = status_media_object
            print("---- IMAGE MEDIA OBJECT STATUS -----\n")
            print("     Status Code:")
            print("     " + media_response['status'])
            sleep(delay)
        """Опубликовать медиа объект"""
        response_media_object = self.__posting_media(media_id)
        posting_limit = self.get_limit_posting_content()
        return response_media_object, posting_limit

    def __create_media(self, image, caption, type_media='img'):

        url = self.params['endpoint_base'] + self.params['instagram_account_id'] + '/media'
        endpoint_data = dict()
        endpoint_data['caption'] = caption
        endpoint_data['access_token'] = self.params['access_token']
        if type_media == 'img':
            endpoint_data['image_url'] = image
        else:
            endpoint_data['media_type'] = "VIDEO"
            endpoint_data['video_url'] = self.params['media_url']
        response = {'data': self.__api_call(url, endpoint_data, 'POST'),
                    'status': 'IN_PROGRESS'}
        return response

    def get_status_media_object(self, created_object_id):
        url = self.params['endpoint_base'] + '/' + created_object_id
        endpoint_data = dict()
        endpoint_data['fields'] = 'status_code'
        endpoint_data['access_token'] = self.params['access_token']
        response = self.__api_call(url, endpoint_data, 'GET')
        return response['json_data']['status_code']

    def __posting_media(self, created_object_id):
        url = self.params['endpoint_base'] + self.params['instagram_account_id'] + '/media_publish'
        endpoint_data = dict()
        endpoint_data['creation_id'] = created_object_id
        endpoint_data['access_token'] = self.params['access_token']
        return self.__api_call(url, endpoint_data, 'POST')

    def get_limit_posting_content(self):
        url = self.params['endpoint_base'] + self.params['instagram_account_id'] + '/content_publishing_limit'
        endpoint_data = dict()
        endpoint_data['fields'] = 'config,quota_usage'
        endpoint_data['access_token'] = self.params['access_token']
        return self.__api_call(url, endpoint_data, 'GET')


api = InstagramApi({'instagram_account_id': '17841403220449260',
                    'access_token': 'EAAGpsNw9iWoBAEWZAeMU57Rps7rslZC4Gf0btFUDLdtLtR5kjXOFZC8HVYhuyU4TNW8OtCLrkPyrbMiuT2d9bZCeXtK0lepLaolcT3Ffcx6JbOXVONZCNFyNjsh9R1JLCEwj9Q5bplatFTZCSW6Fk5I905XUyZA9NZB8bCTa9NIqy682qLi6mJO4TYyg2kPqZBwHF0ByOZBxfwTBCi8DQTenZAyk0TlJNZBZCe6L0qCNZABWmR8rN21wiRRretioWgF7VsIEMZD'})

api.make_post({'image': 'https://images-na.ssl-images-amazon.com/images/I/91m9UMB4p5L._SX500_.jpg',
               'caption': 'v2'})
