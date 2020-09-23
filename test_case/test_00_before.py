from ddt import ddt, data   # 数据类型必须是列表嵌套列表，或者列表嵌套字典
import unittest
from tools.http_request import HttpRequest
import tools.api_logging
from tools.project_path import *
from tools.do_excel import DoExcel
import logging
from tools.common import StartBefore
import os

StartBefore().login()


@ddt
class TestHttpRequest(unittest.TestCase):
    test_data_receipt = DoExcel.get_data(test_data_path, 'start_before')
    current_path = os.path.basename(__file__)

    @data(*test_data_receipt)
    def test_before(self, item):
        test_tesult = None
        r = HttpRequest.http_request(item['url'], eval(item['data']), item['http_method'], eval(item['header']))
        res = r.json()
        # print(res_val)
        try:
            self.assertEqual(item['msg'], res['msg'])
            # print(res.json())
            test_tesult = 'PASS'

            # 将tk写入init文件中
            if 'tk' in res['val']:
                StartBefore().write_back_init(test_tmp_path, 'init', 6, res['val']['tk'])

            # 将新建的顾客写入到test文件的init表中
            if 'id' in res['val']:
                StartBefore().write_back_init(test_tmp_path, 'init', 1, res['val']['id'])

            # 将新建的员工写入到test文件的init表中
            StartBefore().write_employee_id(res)

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












