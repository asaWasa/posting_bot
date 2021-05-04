NONE = None


class KEY:
    API = 'api_key'


class USER_DATA:
    ID = 'id'
    IS_BOT = 'is_bot'
    FIRST_NAME = 'first_name'
    USERNAME = 'username'
    LANGUAGE_CODE = 'language_code'
    ADMIN_RULE = 'admin_rule'
    SOCIAL_NET = 'social_network'
    TIME = 'time'


class RIGHT:
    USER = 0
    MODERATOR = 1
    ADMIN = 2


class INVITE:
    INVITE_KEY = 'invite_key'


class SOCIAL_NETWORK:
    INSTAGRAM = 'instagram'
    VK = 'vk'
    TWITTER = 'twitter'
    YOUTUBE = 'youtube'
    TELEGRAM = 'telegram'


class MONGO_DATA:
    DB_NAME = 'posting_bot'
    DB_COLLECTION_USER = 'users'
    DB_COLLECTION_INVITE = 'invite_keys'
    DB_COLLECTION_REQUEST = 'requests'


class INSTAGRAM:
    MAIN_REQUEST_API = "https://graph.facebook.com/"
    MAIN_PAGE_BROWSER = "https://business.facebook.com/creatorstudio/?tab=instagram_content_posts"
