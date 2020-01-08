import os
import glob

from conf import conf
from model.mysql import init_db

model_mysql_dir = os.path.join(conf.path.work_dir, 'model', 'mysql')


def import_all_mysql_models():
    for file_path in glob.glob('{}/*'.format(model_mysql_dir)):
        basename = os.path.basename(file_path)
        if basename.startswith('_'):
            continue

        name, _ = os.path.splitext(basename)
        module_name = '{}.{}.{}'.format(
            'model',
            'mysql',
            name
        )
        print(module_name)
        __import__(module_name)


def create_table():
    import_all_mysql_models()
    init_db()


if __name__ == '__main__':
    create_table()