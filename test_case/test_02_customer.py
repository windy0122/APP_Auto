from ddt import ddt, data   # 数据类型必须是列表嵌套列表，或者列表嵌套字典
import unittest
from tools.http_request import HttpRequest
import tools.api_logging
from tools.project_path import *
from tools.do_excel import DoExcel
import logging
from tools.common import StartBefore
import os


@ddt
class TestHttpRequest(unittest.TestCase):
    current_path = os.path.basename(__file__)
    test_data_receipt = DoExcel.get_data(test_data_path, 'customer')

    @data(*test_data_receipt)
    def test_customer(self, item):
        test_tesult = None
        r = HttpRequest.http_request(item['url'], eval(item['data']), item['http_method'], eval(item['header']))
        res = r.json()
        # print(res_val)
        try:
            self.assertEqual(item['msg'], res['msg'])
            # print(res.json())
            test_tesult = 'PASS'

            # 通过顾客卡接口，将顾客卡id，写入到init表中
            StartBefore().write_customer_card_id(res)

        except AssertionError as e:
            test_tesult = 'FAILED'
            logging.exception('执行出错：{0}'.format(e))
            # print(res.json())
            raise e
        finally:
            StartBefore.write_back(test_tmp_path, 'test_result', int(item['case_id']),
                                   int(item['case_id']) + 1, str(res), test_tesult, self.current_path)
            logging.info('获取的结果是：{0}'.format(res['msg']))
            logging.info('request:{0}'.format(item))
            logging.info('response:{0}'.format(res))












