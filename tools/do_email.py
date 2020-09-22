import yagmail
from tools.project_path import *
import time


class DoEmail(object):
    @staticmethod
    def send_email():
        yag = yagmail.SMTP(
            user='windy_wudi@163.com',
            password='RWRGOKBMZZQKJUEK',
            host='smtp.163.com'
        )

        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        contents = ['测试报告'+time_now]

        yag.send('575093904@qq.com', '接口自动化测试报告', contents, [test_report_path])

        yag.close()


if __name__ == '__main__':
    DoEmail().send_email()
