import random
import logging
import requests
import json
import time
from tools.project_path import *
from tools.file_is_exists import TestIsExists
from tools.read_config import ReadConfig

url_conf = ReadConfig().get_config(test_config_path, 'URL', 'url')
url_pfm = ReadConfig().get_config(test_config_path, 'URL', 'url_pfm_uat')


class StartBefore(object):
    shop_tk = None
    shop_id = None
    TestIsExists().test_is_exists()
    # shop_customer = None

    # 登录获取店铺tk和shop_id
    # 将token写入init表中
    def login(self):
        global shop_id
        url = url_conf + '/api/rts/base/home/login/V141'

        header_login = {'content-type': 'application/json',
                  'version': '1.4.1',
                  'platform': 'iOS'
                  }

        payload = {
                "smsCodeToken": None,
                "standbyUniqueIdentification": "_Android10",
                "deviceUniqueIdentification": "",
                "password": "e10adc3949ba59abbe56e057f20f883e",
                "loginType": "1",
                "smsCode": None,
                "loginCode": "13411111111",
                "source": "",
                "applicationId": "AjwG1Pb2_9CZbEZ3QnWIc1f7HRbPBXo6-ismtWk5Y27H"
            }

        try:
            r = requests.post(url, headers=header_login, data=json.dumps(payload), verify=False)
            res = r.json()
            shop_tk = res['val']['tk']
            shop_id = res['val']['shopId']
            self.write_back_init(test_tmp_path, 'init', 6, shop_tk)
        except Exception as e:
            logging.info('登录失败')
            raise e
        finally:
            return shop_id

    # pfm登录
    def login_pfm(self):
        url_login_pfm = url_pfm + '/api2/pfm/auth/login'

        header = {
            'platform': 'Web',
            'version': '1.5.0',
            'Content-Type': 'application/json;charset=UTF-8'
        }

        payload = {
            "cellPhoneNumber": "wudi",
            "passwordSHA1": "7c4a8d09ca3762af61e59520943dc26494f8941b"
        }

        try:
            r = requests.post(url_login_pfm, headers=header, data=json.dumps(payload), verify=False)
            res = r.json()
            pfm_tk = res['val']
            self.write_back_init(test_tmp_path, 'init', 10, pfm_tk)
        except Exception as e:
            logging.error('登录失败')
            raise e

    # 随机生成顾客手机号
    @staticmethod
    def create_phone():
        prelist = ['13', '14', '15', '16', '17', '18', '19']
        new_phone_num = random.choice(prelist) + ''.join(random.choice('0123456789') for i in range(9))
        return new_phone_num

    # 获取init表中数据(1、顾客id   2、储值卡id   3、计次卡id    4、年卡id    5、员工id    6、店铺tk
    #  7、储值卡模板id       8、计次卡模板id       9、年卡模板id    10、pfm后台tk      11、玫瑰券id    12、新客券模板id)
    # 13、上下架apply_id
    @staticmethod
    def get_data_init(num):
        wb = openpyxl.load_workbook(test_tmp_path)
        sheet = wb['init']
        init_data = sheet.cell(2, num).value
        if init_data is None:
            init_data = '1'
        return init_data

    # 写入result(返回数据)，写入TestResult(pass or failed)
    @staticmethod
    def write_back(file_name, sheet_name, case_id, i, result, TestResult, current_path):
        wb = openpyxl.load_workbook(file_name)
        sheet = wb[sheet_name]
        sheet.cell(i, 1).value = case_id
        sheet.cell(i, 2).value = result
        sheet.cell(i, 3).value = TestResult
        sheet.cell(i, 4).value = current_path
        wb.save(file_name)

    # 写入数据到init表中
    @staticmethod
    def write_back_init(file_name, sheet_name, i, result):
        wb = openpyxl.load_workbook(file_name)
        sheet = wb[sheet_name]
        sheet.cell(2, i).value = result
        wb.save(file_name)

    # 将新建的员工id写入到init表中
    def write_employee_id(self, res):
        if isinstance(res['val'], list) and len(res['val']) > 1:
            self.write_back_init(test_tmp_path, 'init', 5, res['val'][1]['employeeId'])

    # 获取当前时间时间戳
    @staticmethod
    def get_time_now():
        time_now = round(time.time()*1000)
        return str(time_now)

    # 新建员工
    def before_test_new_employee(self):
        url_new_employee = url_conf + '/api/rts/base/employee/saveEmployee4Shop/V141'

        header = {'content-type': 'application/json',
                  'version': '1.4.1',
                  'platform': 'iOS',
                  'tk': self.get_data_init(6)
                  }

        payload = {
                 "employeeId": "",
                 "roleId": "2",
                 "renewalCardYn": "1",
                 "employeeNickName": "剑琅联盟",
                 "createActivitiesStatus": "1",
                 "scoreSettleStatus": "1",
                 "basicSalary": "1000",
                 "viewCellphoneNumberYn": "1",
                 "employeeMobile": self.create_phone(),
                 "positionId": "2",
                 "workStatus": "0",
                 "scanCouponStatus": "1",
                 "consumeViewStatus": "1",
                 "sellCardYn": "1"
                }

        r = requests.post(url_new_employee, headers=header, data=json.dumps(payload), verify=False)

        res = r.json()
        # print(res)

        self.write_employee_id(res)

    # 获取员工列表
    def before_test_employee_list(self):
        url_employee_list = url_conf + '/api/rts/base/employee/getEmployeeList'

        header = {'content-type': 'application/json',
                  'version': '1.4.1',
                  'platform': 'iOS',
                  'tk': self.get_data_init(6)
                  }

        r = requests.get(url_employee_list, headers=header, verify=False)

        res = r.json()
        # print(res)

        self.write_employee_id(res)


if __name__ == '__main__':
    start = StartBefore()
    start.login()
    start.login_pfm()
    # print(start.test_is_exists())
    # print(start.new_customer_phone())
    # print(start.get_data_init(6))
    # print(start.get_time_now())







