from ddt import ddt, data   # 数据类型必须是列表嵌套列表，或者列表嵌套字典
import unittest
from tools.http_request import HttpRequest
import tools.api_logging
from tools.project_path import *
from tools.do_excel import DoExcel
import logging
from tools.common import StartBefore

test_data_receipt = DoExcel.get_data(test_data_path, 'receipt')


@ddt
class TestHttpRequest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @data(*test_data_receipt)
    def test_receipt(self, item):
        test_tesult = None
        r = HttpRequest.http_request(item['url'], eval(item['data']), item['http_method'], eval(item['header']))
        res = r.json()
        # print(res_val)
        try:
            self.assertEqual(item['msg'], res.json()['msg'])
            print(res.json())
            test_tesult = 'PASS'

        except AssertionError as e:
            test_tesult = 'FAILED'
            logging.exception('执行出错：{0}'.format(e))
            print(res.json())
            raise e
        finally:
            StartBefore.write_back(test_data_path, item['sheet_name'], int(item['case_id']) + 1, str(res), test_tesult)
            logging.info('获取的结果是：{0}'.format(res.json()['msg']))












