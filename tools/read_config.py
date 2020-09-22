import configparser
from tools.project_path import *


class ReadConfig(object):

    @staticmethod
    def get_config(file_path, section, option):
        cf = configparser.ConfigParser()
        cf.read(file_path)
        return cf[section][option]


if __name__ == '__main__':
    config_info = ReadConfig()
    # print(config_info.get_config(test_config_path, 'URL', 'uat_url'))
    # config_info.get_config(test_config_path, 'MODE', 'mode')
    print(config_info.get_config(test_config_path, 'MODE', 'mode'))

