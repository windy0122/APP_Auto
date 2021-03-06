from ddt import ddt, data   # 数据类型必须是列表嵌套列表，或者列表嵌套字典
import unittest
from tools.http_request import HttpRequest
import tools.api_logging
from tools.project_path import *
from tools.do_excel import DoExcel
import logging
from tools.common import StartBefore
import os


current_path = os.path.basename(__file__)

test_data_card_template = DoExcel.get_data(test_data_path, 'create_card_template')
# print(test_data_card_template)


@ddt
class TestCreateCardTemplate(unittest.TestCase):
    # test_data_delete_card_template = DoExcel.get_data(test_data_path, 'card_template')

    @data(*test_data_card_template)
    def test_card_template(self, item):
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
            # 将卡模板id，写入init表中
            StartBefore().get_card_template()
            logging.info('request:{0}'.format(item))
            logging.info('response:{0}'.format(res))


if __name__ == '__main__':
    TestCreateCardTemplate().get_card_data()






