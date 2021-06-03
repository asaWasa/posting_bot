NONE = None


class KEY:
    API = 'api_key'


class SOCIAL_NETWORKS:
    INSTAGRAM = 'instagram'
    VK = 'vk'
    TWITTER = 'twitter'
    YOUTUBE = 'youtube'
    TELEGRAM = 'telegram'
    TIKTOK = 'tiktok'


class USER_DATA:
    ID = 'id'
    IS_BOT = 'is_bot'
    FIRST_NAME = 'first_name'
    USERNAME = 'username'
    LANGUAGE = 'language_code'
    RIGHTS = 'rule'
    SOCIAL_NETWORK = 'social_network'
    QUOTAS_USAGE = {SOCIAL_NETWORKS.INSTAGRAM: 0,
                    SOCIAL_NETWORKS.VK: 0,
                    SOCIAL_NETWORKS.TWITTER: 0,
                    SOCIAL_NETWORKS.TIKTOK: 0,
                    SOCIAL_NETWORKS.YOUTUBE: 0,
                    SOCIAL_NETWORKS.TELEGRAM: 0
                    }
    TIME = 'time'


# todo вынести в отдельный файл
class UserRequest:
    Id_request = 'id_request'
    User_id = 'user_id'
    Type_request = 'type_request'
    Data_object = 'data_object'
    Name = 'name'
    Date_creation = 'date_creation'


# todo вынести в отдельный файл
class UserTypeRequest:
    Post_image = 'POST_IMAGE'
    Post_video = 'POST_VIDEO'


class RIGHTS:
    USER = 0
    MODERATOR = 1
    ADMIN = 2
    TESTER = 3


class INVITE:
    KEY = 'key'


class MongoData:
    db_main = 'posting_bot'
    db_queues = 'queues'

    db_collection_user = 'users'
    db_collection_invite = 'invite_keys'
    db_collection_requests = 'users_requests'
    db_collection_main_queue = 'main_queue'


class Instagram:
    main_endpoint_request_api = "https://graph.facebook.com/"


class QUEUES:
    QUEUE = 'queue'
    INSTAGRAM = SOCIAL_NETWORKS.INSTAGRAM + QUEUE
    TWITTER = SOCIAL_NETWORKS.TWITTER + QUEUE
    TIKTOK = SOCIAL_NETWORKS.TIKTOK + QUEUE
    YOUTUBE = SOCIAL_NETWORKS.YOUTUBE + QUEUE
    VK = SOCIAL_NETWORKS.VK + QUEUE


class RequestType:
    POST = 'POST'
    GET = 'GET'

