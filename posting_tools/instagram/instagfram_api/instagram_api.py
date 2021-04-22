import requests


class ApiInstagram:
    def __init__(self, user_data_object):
        self.login = user_data_object['login']
        self.password = user_data_object['password']
        self.business_id = user_data_object["instagram_business_id"]
        self.access_token = user_data_object["facebook_page_access_token"]

    def make_post(self, image, caption):
        image = self.__convert_image_to_jpg(image)
        creation_id = self.__create_media_object(image, caption)
        stat = self.__publishing_media_object(creation_id)
        print(stat)

    def __convert_image_to_jpg(self, image):
        return image

    def __create_media_object(self, image, caption):
        req = "https://graph.facebook.com/{}/media?image_url={}&caption={}&access_token={}".format(self.business_id,
                                                                                                   image, caption,
                                                                                                   self.access_token)
        creation_id = requests.request(method="post", url=req)
        return creation_id

    def __publishing_media_object(self, creation_id):
        req = "https://graph.facebook.com/{}/media_publish?creation_id={}&access_token={}".format(self.business_id,
                                                                                                  creation_id,
                                                                                                  self.access_token)
        stat = requests.request(method="post", url=req)
        return stat
