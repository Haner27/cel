from hashlib import md5

from util.error_code import VerifyError

key_pairs = {'cel_ddS0gFEJJxGRE1lK', '4M7oXIE7HdRecv21qGbA9BrRYHtUpxKF'}


class Signature:
    SIGN_FILED_NAME = 'sign'
    APP_KEY_FILED_NAME = 'app_key'
    SECRET_KEY_FILED_NAME = 'secret_key'

    """数字签名"""
    def __init__(self):
        pass

    def get_sorted_pair_str(self, **kwargs):
        l = []
        for k, v in sorted(kwargs.items(), key=lambda a: a[0]):
            if k == self.SIGN_FILED_NAME:
                continue

            l.append(f'{k}={v}')
        return '&'.join(l)

    def signature(self, **kwargs):
        app_key = kwargs.get(self.APP_KEY_FILED_NAME, '')
        secret_key = key_pairs.get(app_key, '')
        sorted_pair_str = self.get_sorted_pair_str(**kwargs) + secret_key
        return md5(sorted_pair_str.encode('utf-8')).hexdigest()

    def verify(self, **kwargs):
        if self.SIGN_FILED_NAME not in kwargs:
            raise VerifyError(VerifyError.ERROR_LACK_SIGNATURE)

        if self.APP_KEY_FILED_NAME not in kwargs:
            raise VerifyError(VerifyError.ERROR_LACK_APP_KEY)

        sign = kwargs.get('sign', '')
        sign_new = self.signature(**kwargs)
        if sign != sign_new:
            raise VerifyError(VerifyError.ERROR_VERIFY_FAILED)
        return True


signature_instance = Signature()


if __name__ == '__main__':
    data = {
        'app_key': 'cel_ddS0gFEJJxGRE1lK',
        'name': 'han',
        'age': 27,
        'gender': 'male'
    }
    s = signature_instance
    sign = s.signature(**data)
    print(sign)

    import copy  # str byte

    d1 = copy.deepcopy(data)
    d1.update(sign=sign)
    try:
        s.verify(**d1)
    except Exception as e:
        print(e)
    else:
        print('passed.')

    d2 = copy.deepcopy(data)
    d2.update(sign1=sign)
    try:
        s.verify(**d2)
    except Exception as e:
        print(e)
    else:
        print('passed.')

    d3 = copy.deepcopy(data)
    d3.update(sign=sign + '1')
    try:
        s.verify(**d3)
    except Exception as e:
        print(e)
    else:
        print('passed.')
