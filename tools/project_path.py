# 专门读取路径的值

import os
import logging
import openpyxl

# project_path = os.path.realpath(__file__)  # D:\Api_Auto\tools\project_path.py
project_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]    # D:\Api_Auto

# 测试用例路径(读取)
test_data_path = os.path.join(project_path, 'test_data', 'test.xlsx')     # D:\Api_Auto\test_data\uat_data.xlsx

# 测试中间路径(写入)
test_tmp_path = os.path.join(project_path, 'test_data', 'testtmp.xlsx')

# 测试报告路径
test_report_path = os.path.join(project_path, 'test_result', 'html_report', 'test_report.html')

# 测试模块路径
test_config_path = os.path.join(project_path, 'conf', 'case.config')

# log路径
test_log_path = os.path.join(project_path, 'test_result', 'log', 'logging.log')


if __name__ == '__main__':
    print(test_tmp_path)




