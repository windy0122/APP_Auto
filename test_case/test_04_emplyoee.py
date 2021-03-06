from ddt import ddt, data   # 数据类型必须是列表嵌套列表，或者列表嵌套字典
import unittest
from tools.http_request import HttpRequest
import tools.api_logging
from tools.project_path import *
from tools.do_excel import DoExcel
import logging
from tools.common import StartBefore
# from tools.start_before import StartBefore
import os

StartBefore().before_test_new_employee()

current_path = os.path.basename(__file__)


@ddt
class TestHttpRequest(unittest.TestCase):
    test_data = DoExcel.get_data(test_data_path, 'employee')

    @data(*test_data)
    def test_employee(self, item):
        test_tesult = None
        r = HttpRequest.http_request(item['url'], eval(item['data']), item['http_method'], eval(item['header']))
        res = r.json()
        # print(res_val)
        try:
            self.assertEqual(item['msg'], res['msg'])
            # print(res.json())
            test_tesult = 'PASS'

        except AssertionError as e:
            test_tesult = 'FAILED'
            logging.exception('执行出错：{0}'.format(e))
            # print(res.json())
            raise e
        finally:
            StartBefore.write_back(test_tmp_path, 'test_result', int(item['case_id']),
                                   int(item['case_id']) + 1, str(res), test_tesult, current_path)
            logging.info('获取的结果是：{0}'.format(res['msg']))
            logging.info('request:{0}'.format(item))
            logging.info('response:{0}'.format(res))








