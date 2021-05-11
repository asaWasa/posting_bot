from time import sleep
import requests
import json
from common.constants import RequestType, UserRequest

from common.errors import *


class InstagramApi:
    def __init__(self, user_object):
        self.params = self.__get_user_param(user_object)

    def __get_user_param(self, user_object):
        # todo есть вероятность, что версия изменится, придумать как проверять версию api
        data = self.__get_user_data(user_object)
        user_param = dict()
        user_param['access_token'] = data['access_token']
        user_param['endpoint_base'] = 'https://graph.facebook.com/v10.0/'
        user_param['instagram_account_id'] = data['instagram_account_id']
        return user_param

    def __get_user_data(self, user_data) -> dict:
        """Получить access_token и instagram_account_id пользователя"""
        user_data = user_data['data_object']
        data = dict()
        data['access_token'] = user_data['access_token']
        data['instagram_account_id'] = user_data['instagram_account_id']
        return data

    def __api_call(self, url, endpoint_data, request_type) -> dict:
        if request_type == RequestType.POST:
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

    def make_post(self, user_request, delay=5):
        try:
            """создать медиа объект"""
            media_response = self.__create_media(user_request['image'], user_request['caption'])
            media_id = media_response['data']['json_data']
            while media_response['status'] != 'FINISHED':
                status_media_object = self.get_status_media_object(media_id)
                media_response['status'] = status_media_object
                print("---- IMAGE MEDIA OBJECT STATUS -----")
                print("     Status Code:")
                print("     " + media_response['status'])
                sleep(delay)
            """Опубликовать медиа объект"""
            response_media_object = self.__posting_media(media_id)
            posting_limit = self.get_limit_posting_content()
            # todo переделать ответ в dict
            print("---- POSTING MEDIA OBJECT STATUS -----")
            print("     ID:")
            print("     " + str(response_media_object['json_data']))
            print("     POSTING LIMIT USAGE:")
            print("     " + str(posting_limit['json_data']))
            return response_media_object, posting_limit

        except NoValidToken:
            # todo вернуть ошибку выше
            pass
        except BadImage:
            # todo вернуть ошибку выше
            pass
        except BadCaption:
            # todo вернуть ошибку выше
            pass
        except Exception as e:
            # todo вернуть ошибку выше
            print('error - {}'.format(e))
            pass

    def __create_media(self, image, caption, type_media='img'):
        try:
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
            self.__check_response_errors(response)
            return response
        # todo добавить логгирование
        except NoValidToken:
            print('---------------ERROR TOKEN---------------')
            raise NoValidToken
        except BadImage:
            print('---------------ERROR IMAGE---------------')
            raise BadImage
        except BadCaption:
            print('---------------ERROR CAPTION---------------')
            raise BadCaption
        except Exception as e:
            print('error media - {}'.format(e))
            raise e

    def __check_response_errors(self, data):
        try:
            data = data['data']['json_data']['error']
            subcode = data['error_subcode']
            if subcode == 463:
                raise NoValidToken
        except NoValidToken:
            raise NoValidToken
        except:
            pass

    def get_status_media_object(self, created_object_id):
        _id = created_object_id['id']
        url = self.params['endpoint_base'] + '/' + _id
        endpoint_data = dict()
        endpoint_data['fields'] = 'status_code'
        endpoint_data['access_token'] = self.params['access_token']
        response = self.__api_call(url, endpoint_data, 'GET')
        return response['json_data']['status_code']

    def __posting_media(self, created_object_id):
        url = self.params['endpoint_base'] + self.params['instagram_account_id'] + '/media_publish'
        endpoint_data = dict()
        endpoint_data['creation_id'] = created_object_id['id']
        endpoint_data['access_token'] = self.params['access_token']
        return self.__api_call(url, endpoint_data, 'POST')

    def get_limit_posting_content(self):
        url = self.params['endpoint_base'] + self.params['instagram_account_id'] + '/content_publishing_limit'
        endpoint_data = dict()
        endpoint_data['fields'] = 'config,quota_usage'
        endpoint_data['access_token'] = self.params['access_token']
        return self.__api_call(url, endpoint_data, 'GET')


# api = InstagramApi({'instagram_account_id': '17841403220449260',
#                     'access_token': 'EAAGpsNw9iWoBANRukZBWRBkXLUOsZBqa95BdYy0mqVvfmUSU29tfQRYVgcesZCcZAZCIf0uZA0BNHZCsUth5kdSvUL7LAKuZAuaIhsQImei2lycWnmsvnnIl8FqGE6Df04kXelQTjoXd0Kl2DZBEMUQs9RrsAVGjhNMZB37rnTaAFFKmexLP14fkfbWr02qILuPI148JhXSLphLrwD6UvgkuZB6yxZBxHo6tDciYCv6yYMq2vERQagqlj5e2JoOM2nOF3QcZD'})
#
# api.make_post({'image': 'https://api.telegram.org/file/bot1709642482:AAHXAnZ8UBCMeEDuEikCqYBFhkA8MDN7rNk/photos/file_0.jpg',
#                'caption': 'o'})
