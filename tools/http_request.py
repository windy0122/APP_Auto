import requests
import logging
import json


class HttpRequest(object):
    @staticmethod
    def http_request(url, data, http_method, header):
        try:
            if http_method.lower() == 'get':
                r = requests.get(url=url, params=data, headers=header, verify=False)
            elif http_method.lower() == 'post':
                r = requests.post(url=url, data=json.dumps(data), headers=header, verify=False)
            else:
                r = None
                logging.info('输入的请求方法不正确')
        except Exception as e:
            logging.exception('请求报错了：{}'.format(e))
            raise e
        return r

