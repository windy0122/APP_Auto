# from test_case.test_01_receipt import TestHttpRequest
import unittest
from tools.project_path import *
import HTMLTestRunner
from test_case import before
from test_case import test_01_receipt
from test_case import customer
from test_case import test_03_emplyoee
from test_case import test_04_emplyoee_update
from test_case import test_02_customer

# 根据类来执行用例
# suite = unittest.TestSuite()
# loder = unittest.TestLoader()
# suite.addTest(loder.loadTestsFromTestCase(TestHttpRequest))

# 根据测试用例来执行
suite = unittest.TestSuite()
loder = unittest.TestLoader()
# suite.addTest(loder.loadTestsFromModule(before))
suite.addTest(loder.loadTestsFromModule(test_01_receipt))
suite.addTest(loder.loadTestsFromModule(customer))
suite.addTest(loder.loadTestsFromModule(test_02_customer))
suite.addTest(loder.loadTestsFromModule(test_03_emplyoee))
suite.addTest(loder.loadTestsFromModule(test_04_emplyoee_update))


with open(test_report_path, 'wb') as file:
    # runner = HTMLTestRunner_cn.HTMLTestRunner(stream=file, title='自动化测试', description='测试报告', tester='吴迪')
    # runner.run(suite)

    runner = HTMLTestRunner.HTMLTestRunner(stream=file, title='自动化测试', description='自动化测试报告：吴迪')
    runner.run(suite)

# DoEmail().send_email()

