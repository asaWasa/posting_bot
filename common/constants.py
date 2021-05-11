NONE = None


class Key:
    Api = 'api_key'


class UserData:
    Id = 'id'
    Is_bot = 'is_bot'
    First_name = 'first_name'
    Username = 'username'
    Language_code = 'language_code'
    Admin_rule = 'admin_rule'
    Social_net = 'social_network'
    Time = 'time'


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


class Rights:
    User = 0
    Moderator = 1
    Admin = 2


class Invite:
    Invite_key = 'invite_key'


class SocialNetwork:
    Instagram = 'instagram'
    Vk = 'vk'
    Twitter = 'twitter'
    YouTube = 'youtube'
    Telegram = 'telegram'


class MongoData:
    db_main = 'posting_bot'
    db_queues = 'queues'

    db_collection_user = 'users'
    db_collection_invite = 'invite_keys'
    db_collection_requests = 'users_requests'
    db_collection_main_queue = 'main_queue'


class Instagram:
    main_endpoint_request_api = "https://graph.facebook.com/"


class Queues:
    Instagram = 'instagram'


class RequestType:
    POST = 'POST'
    GET = 'GET'
