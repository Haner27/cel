UNKNOWN_CODE = 1000
UNKNOWN_MSG = "未知错误"

class BaseError(Exception):
    ERROR_DICT = dict()
    
    def __init__(self, code):
        if code not in self.ERROR_DICT:
            self.code, self.msg = UNKNOWN_CODE, UNKNOWN_MSG
        else:
            self.code = code
            self.msg = self.ERROR_DICT.get(code)
        self.message = f"[{self.code}] {self.msg}"

    def __str__(self):
        return self.message

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, self.message)


class VerifyError(BaseError):
    ERROR_LACK_SIGNATURE = 1001
    ERROR_VERIFY_FAILED = 1002
    ERROR_NOT_JSON_DATA = 1003
    ERROR_LACK_APP_KEY = 1004
    ERROR_DICT = {
        ERROR_LACK_SIGNATURE: "缺少参数sign",
        ERROR_VERIFY_FAILED: "验证签名失败",
        ERROR_NOT_JSON_DATA: "参数错误：仅支持json数据",
        ERROR_LACK_APP_KEY: "缺少参数app_key",
    }


class LoaderError(BaseError):
    ILLEGAL_ID = 4001
    NOT_FOUND = 4002
    NOT_SUPPORTED = 4003
    ERROR_DICT = {
        ILLEGAL_ID: "illegal qid",
        NOT_FOUND: "qid not found",
        NOT_SUPPORTED: "qid not supported",
    }
