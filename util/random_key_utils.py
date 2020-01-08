import random
from itertools import chain

charsets = chain(
    [chr(n) for n in range(48, 58)],
    [chr(u) for u in range(65, 91)],
    [chr(l) for l in range(97, 123)]
)
charsets = list(charsets)
random.shuffle(charsets)


def get_random_str(length=0):
    if not length:
        return ''
    l = random.choices(charsets, k=length)
    return ''.join(l)


def create_a_key_pair(app_name):
    app_key = 'cel_' + get_random_str(16)
    secret_key = get_random_str(32)
    return {
        app_name: {
            'app_key': app_key,
            'secret_key': secret_key
        }
    }


if __name__ == '__main__':
    key_pair = create_a_key_pair('tx')
    print(key_pair)