from common.constants import USER_DATA, RIGHTS, NONE


class UserDataFormat:
    def __init__(self, data):
        self.data = dict(data)

    def to_dict(self):
        result = dict()
        result[USER_DATA.TIME] = 0
        result[USER_DATA.ID] = self.data[USER_DATA.ID]
        result[USER_DATA.IS_BOT] = self.data[USER_DATA.IS_BOT]
        result[USER_DATA.FIRST_NAME] = self.data[USER_DATA.FIRST_NAME]
        result[USER_DATA.USERNAME] = self.data[USER_DATA.USERNAME]
        result[USER_DATA.LANGUAGE] = self.data[USER_DATA.LANGUAGE]
        result[USER_DATA.RIGHTS] = RIGHTS.USER
        result[USER_DATA.SOCIAL_NETWORK] = dict()

        return result
