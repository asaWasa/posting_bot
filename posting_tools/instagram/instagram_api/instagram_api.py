from time import sleep
import requests
import json
from common.constants import RequestType

from common.errors import *


class InstagramApi:
    def __init__(self, user_object, log=None):
        try:
            self.log = log
            self.params = self.__get_user_param(user_object)
        except:
            self.log.info("__init__ ERROR")

    def __get_user_param(self, user_object):
        # todo есть вероятность, что версия изменится, придумать как проверять версию api
        try:
            data = self.__get_user_data(user_object)
            user_param = dict()
            user_param['access_token'] = data['access_token']
            user_param['endpoint_base'] = 'https://graph.facebook.com/v10.0/'
            user_param['instagram_account_id'] = data['instagram_account_id']
            return user_param
        except:
            raise UserParamError

    def __get_user_data(self, user_data) -> dict:
        """Получить access_token и instagram_account_id пользователя"""
        data = dict()
        data['access_token'] = user_data['token']
        data['instagram_account_id'] = user_data['business_id']
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
            user_data = self.__get_request_data(user_request)
            media_response = self.__create_media(user_data['image'], user_data['caption'])
            media_id = media_response['data']['json_data']
            while media_response['status'] != 'FINISHED':
                status_media_object = self.get_status_media_object(media_id)
                media_response['status'] = status_media_object
                self.log.info('User {}; Media Status {}'.format(user_request['user_id'],
                                                                status_media_object))
                sleep(delay)
            """Опубликовать медиа объект"""
            response_media_object = self.__posting_media(media_id)
            posting_limit = self.get_limit_posting_content()
            response_media_object = response_media_object['json_data']['id']
            posting_limit = posting_limit['json_data']['data'][0]

            self.log.info('User {}; Posting media id {}; Quota limit {}'
                          .format(user_request['user_id'],
                                  str(response_media_object['json_data']),
                                  str(posting_limit)))
            result = {'response': response_media_object, 'quota_usage': posting_limit}
            return result

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
            self.log('error - {}'.format(e))
            pass

    def __get_request_data(self, request):
        return request['data_object']

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
        except NoValidToken:
            self.log.info('Error token')
            raise NoValidToken
        except BadImage:
            self.log.info('Error image')
            raise BadImage
        except BadCaption:
            self.log.info('Error caption')
            raise BadCaption
        except Exception as e:
            self.log.info('error media - {}'.format(e))
            raise e

    def __check_response_errors(self, data):
        try:
            data = data['data']['json_data']['error']
            subcode = data['error_subcode']
            if subcode == 463:
                raise NoValidToken
        except NoValidToken:
            raise NoValidToken
        except Exception as e:
            raise e

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
