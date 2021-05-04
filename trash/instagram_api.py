import requests
import json


class ApiInstagram:
    def __init__(self, user_data_object):
        self.business_id = user_data_object["instagram_business_id"]
        self.user_access_token = self.__get_user_access_tocen(user_data_object)

    def __get_user_access_tocen(self, user_data_object):
        return user_data_object["user_access_token"]

    def make_post(self, image, caption):
        image = self.__convert_image_to_jpg(image)
        raw_json_creation_id = self.__create_media_object(image, caption)
        creation_id = self.__clear_id(raw_json_creation_id)
        stat = self.__publishing_media_object(creation_id)
        print(stat.text)

    def __convert_image_to_jpg(self, image):
        return image

    def __clear_caption(self, caption):
        return caption

    def __create_media_object(self, image, caption, location=None, date=None):
        req = "https://graph.facebook.com/v10.0/{}/media".format(self.business_id)
        data = {
            "image_url": image,
            "caption": caption,
            "access_token": self.user_access_token
        }
        creation_id = requests.post(req, data=data)
        return creation_id.text

    def __publishing_media_object(self, creation_id):
        req = "https://graph.facebook.com/{}/media_publish".format(self.business_id)
        data = {
            "creation_id": creation_id,
            'access_token': self.user_access_token
        }
        stat = requests.post(req, data=data)
        return stat

    def __clear_id(self, raw_json_creation_id):
        try:
            return json.loads(raw_json_creation_id)
        except Exception as e:
            print('Ошибка очистки "creation id" {}'.format(e))


api = ApiInstagram({'instagram_business_id': '17841403220449260',
                    'user_access_token': "EAAGpsNw9iWoBAGVGDhra6AZBGu99cmaxc3g3BvrJOanp2HIb3FgOb4lqrCQLGYs2Oe0uECxl4zrrZBIjejsMmPuo2OeyiZA6XUTlJaTyXZBk0MwJETso44GC5YDQHwmZBZCeJfO0t0VsiLUtOWlP7Bnpf05MjfStj1SHpF8VXU4TbuT2SXox0z3dpDkcIJiqKlBgrTTOK7ZCyKiQahEKMXY58jBJw22I34QlnWjrOckQJo1fstDtPZAx2xnEIJOQrG4ZD"})
api.make_post('1.jpg', 'test')
