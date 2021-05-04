from common.constants import USER_DATA, RIGHT, NONE


class USER_FORMAT:
    def __init__(self, data):
        self.data = dict(data)

    def to_dict(self):
        result = dict()
        result[USER_DATA.TIME] = 0
        result[USER_DATA.ID] = self.data[USER_DATA.ID]
        result[USER_DATA.IS_BOT] = self.data[USER_DATA.IS_BOT]
        result[USER_DATA.FIRST_NAME] = self.data[USER_DATA.FIRST_NAME]
        result[USER_DATA.USERNAME] = self.data[USER_DATA.USERNAME]
        result[USER_DATA.LANGUAGE_CODE] = self.data[USER_DATA.LANGUAGE_CODE]
        result[USER_DATA.ADMIN_RULE] = RIGHT.USER
        result[USER_DATA.SOCIAL_NET] = NONE

        return result
