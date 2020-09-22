from ddt import ddt, data   # 数据类型必须是列表嵌套列表，或者列表嵌套字典
import unittest
from tools.http_request import HttpRequest
import tools.api_logging
from tools.project_path import *
from tools.do_excel import DoExcel
import logging
from tools.common import StartBefore

# my_logger = MyLog()
test_data = DoExcel.get_data(test_data_path, 'employee')


@ddt
class TestHttpRequest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @data(*test_data)
    def test_employee(self, item):
        res = HttpRequest.http_request(item['url'], eval(item['data']), item['http_method'], eval(item['header']))
        # res_val = res.json()
        # print(res)
        try:
            self.assertEqual(item['msg'], res.json()['msg'])
            print(res.json())
            TestResult = 'PASS'

            # 将新建的员工写入到test文件的init表中
            StartBefore().write_employee_id(res.json())

        except AssertionError as e:
            TestResult = 'FAILED'
            logging.exception('执行出错：{0}'.format(e))
            print(res.json())
            raise e
        finally:
            StartBefore.write_back(test_data_path, item['sheet_name'], int(item['case_id']) + 1, str(res.json()), TestResult)
            logging.info('获取的结果是：{0}'.format(res.json()['msg']))










