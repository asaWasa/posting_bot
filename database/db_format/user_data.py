from common.constants import USER_DATA, RIGHTS, SOCIAL_NETWORKS, DEFAULT
import datetime


class ElementaryUserDataFormat:
    def __init__(self, data, time=datetime.datetime.now(), id=None, is_bot=None, first_name=None, username=None,
                 language_code=None, rights=RIGHTS.USER, social_network=DEFAULT.SOCIAL_NETWORKS,
                 quota_usage=DEFAULT.QUOTAS, errors=DEFAULT.ERRORS):
        # self.data = dict(data)
        self.time = time
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.username = username
        self.language_code = language_code
        self.rights = rights
        self.social_network = social_network
        self.quota_usage = quota_usage
        self.errors = errors

        if data is not None:
            self.__dict__.update(data)
            return

    def __repr__(self):
        return '{}'.format(self.id)

    def __str__(self):
        return '{}'.format(self.id)

    def to_dict(self):
        result = dict()
        result[USER_DATA.TIME] = self.time
        result[USER_DATA.ID] = self.id
        result[USER_DATA.IS_BOT] = self.is_bot
        result[USER_DATA.FIRST_NAME] = self.first_name
        result[USER_DATA.USERNAME] = self.username
        result[USER_DATA.LANGUAGE] = self.language_code
        result[USER_DATA.RIGHTS] = self.rights
        result[USER_DATA.SOCIAL_NETWORK] = self.social_network
        result[USER_DATA.QUOTAS_USAGE] = self.quota_usage
        result[USER_DATA.ERRORS] = self.errors
        return result


    # def to_dict(self):
    #     result = dict()
    #     result[USER_DATA.TIME] = 0
    #     result[USER_DATA.ID] = self.data[USER_DATA.ID]
    #     result[USER_DATA.IS_BOT] = self.data[USER_DATA.IS_BOT]
    #     result[USER_DATA.FIRST_NAME] = self.data[USER_DATA.FIRST_NAME]
    #     result[USER_DATA.USERNAME] = self.data[USER_DATA.USERNAME]
    #     result[USER_DATA.LANGUAGE] = self.data[USER_DATA.LANGUAGE]
    #     result[USER_DATA.RIGHTS] = RIGHTS.USER
    #     result[USER_DATA.SOCIAL_NETWORK] = DEFAULT.SOCIAL_NETWORKS
    #     result[USER_DATA.QUOTAS_USAGE] = DEFAULT.QUOTAS
    #     return result
