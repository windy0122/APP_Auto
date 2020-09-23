# import openpyxl
# import logging
from tools.project_path import *


class TestIsExists(object):
    # 判断测试中间文件是否存在
    @staticmethod
    def test_is_exists():
        if os.path.exists(test_tmp_path) is False:
            wb = openpyxl.Workbook()
            ws = wb.active

            ws.title = 'init'

            ws['A1'] = '新建顾客id'
            ws['B1'] = '新办储值卡id'
            ws['C1'] = '新办计次卡id'
            ws['D1'] = '新办年卡id'
            ws['E1'] = '新建员工id'
            ws['F1'] = '店铺tk'

            ws_result = wb.create_sheet('test_result')

            ws_result['A1'] = 'case_id'
            ws_result['B1'] = 'result'
            ws_result['C1'] = 'TestResult'
            ws_result['D1'] = 'current_path'

            wb.save(test_tmp_path)
        else:
            logging.info('文件已存在')


if __name__ == '__main__':
    TestIsExists().test_is_exists()


