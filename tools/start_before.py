from tools.common import StartBefore
from tools.read_config import ReadConfig
from tools.project_path import *
import requests
import json
import logging
import tools.api_logging


url_conf = ReadConfig().get_config(test_config_path, 'URL', 'url')


class StartBeforeNew(object):

    header = {'content-type': 'application/json',
              'version': '1.4.1',
              'platform': 'iOS',
              'tk': StartBefore().get_data_init(6)
              }

    # 用例开始前接口
    # 新建卡模板
    def create_card_template(self):
        url_card_template = url_conf + '/api/rts/member/card/addCardTemplate/V141'

        payload = {
             "enjoyDiscount": "90",
             "cardTemplateSourceType": "0",
             "cardType": "1",
             "rechargeAmount": "1000",
             "cardName": "储值卡测试",
             "useMonth": "12",
             "giftAmount": ""
            }

        payload_time = {
            "purchaseTimes": "10",
            "useMonth": "9999",
            "cardType": "2",
            "cardTemplateSourceType": "0",
            "applicableItemId": "5",
            "cardName": "计次卡测试",
            "purchasePrice": "1000"
        }

        payload_year = {
             "cardTemplateSourceType": "0",
             "purchasePrice": "1000",
             "cardName": "年卡测试",
             "cardType": "3",
             "enjoyDiscount": "90"
            }

        r = requests.post(url_card_template, headers=self.header, data=json.dumps(payload), verify=False)
        r_time = requests.post(url_card_template, headers=self.header, data=json.dumps(payload_time), verify=False)
        r_year = requests.post(url_card_template, headers=self.header, data=json.dumps(payload_year), verify=False)

        res = r.json()
        # print(res)
        res_time = r_time.json()
        res_year = r_year.json()

        if res['msg'] == '操作成功':
            logging.info('创建储值卡成功')
        else:
            logging.error('创建储值卡失败')

        if res_time['msg'] == '操作成功':
            logging.info('创建计次卡成功')
        else:
            logging.error('创建计次卡失败')

        if res_year['msg'] == '操作成功':
            logging.info('创建年卡成功')
        else:
            logging.error('创建年卡失败')

        self.get_card_template()

    # 获取卡模板列表
    def get_card_template(self):
        url_card_template = url_conf + '/api/rts/member/card/getCardTemplateList/V131'

        payload = {
            "size": 20,
            "page": 1
        }

        r = requests.post(url_card_template, headers=self.header, data=json.dumps(payload), verify=False)

        res = r.json()

        # 写入卡列表中的卡模板id，
        if isinstance(res['val'], list) and res['val'] != []:
            for i in range(len(res['val'])):
                if res['val'][i]['cardName'] == '储值卡测试':
                    StartBefore().write_back_init(test_tmp_path, 'init', 7, res['val'][i]['id'])
                elif res['val'][i]['cardName'] == '计次卡测试':
                    StartBefore().write_back_init(test_tmp_path, 'init', 8, res['val'][i]['id'])
                elif res['val'][i]['cardName'] == '年卡测试':
                    StartBefore().write_back_init(test_tmp_path, 'init', 9, res['val'][i]['id'])

    # 新建顾客
    def before_test_new_customer(self):
        url_new_customer = url_conf + '/api/rts/member/membership/addMembership/V125'

        payload = {
            "membershipMobile": StartBefore().create_phone(),
            "gender": "0",
            "membershipName": "啦啦啦"
        }

        r = requests.post(url_new_customer, headers=self.header, data=json.dumps(payload), verify=False)

        res = r.json()
        print(res)

        if 'id' in res['val']:
            StartBefore().write_back_init(test_tmp_path, 'init', 1, res['val']['id'])

    # 办理顾客卡
    def new_customer_card(self):
        url_customer_card = url_conf + '/api/rts/member/membershipCard/purchaseNewCard/V141'

        payload_new_store = {
             "rechargeAmount": "1000.0000",
             "systemDictionaryId": "456084858905566471",
             "journalDate": StartBefore().get_time_now(),
             "giftAmount": "0.0000",
             "membershipId": StartBefore().get_data_init(1),
             "employeeIdList": ["343732200062099456"],
             "cardTemplateId": "465599316220481536"
            }

        payload_new_time = {
             "cardTemplateId": "503611922391625728",
             "employeeIdList": ["343732200062099456"],
             "journalDate": StartBefore().get_time_now(),
             "membershipId": StartBefore().get_data_init(1),
             "systemDictionaryId": "456084858905566471",
             "purchaseAmount": "2000.0000"
            }

        payload_new_year = {
             "journalDate": StartBefore().get_time_now(),
             "cardTemplateId": "463767922616791040",
             "employeeIdList": ["343732200062099456"],
             "membershipId": StartBefore().get_data_init(1),
             "systemDictionaryId": "456084858905566471",
             "purchaseAmount": "1000.0000"
            }

        r_store = requests.post(url_customer_card, headers=self.header, data=json.dumps(payload_new_store), verify=False)
        r_time = requests.post(url_customer_card, headers=self.header, data=json.dumps(payload_new_time), verify=False)
        r_year = requests.post(url_customer_card, headers=self.header, data=json.dumps(payload_new_year), verify=False)

        res_store = r_store.json()
        # print(res_store)
        res_time = r_time.json()
        res_year = r_year.json()

        if res_store['msg'] == '操作成功':
            logging.info('顾客办储值卡成功')
        else:
            logging.error('顾客办储值卡失败')

        if res_time['msg'] == '操作成功':
            logging.info('顾客办计次卡成功')
        else:
            logging.error('顾客办计次卡失败')

        if res_year['msg'] == '操作成功':
            logging.info('顾客办年卡成功')
        else:
            logging.error('顾客办年卡失败')

    # 获取顾客卡列表
    def before_test_customer_list(self):
        url_customer_list = url_conf + '/api/rts/member/membershipCard/membershipCardList/V131'

        payload = {
            'id': StartBefore().get_data_init(1)
        }

        r = requests.get(url_customer_list, headers=self.header, params=payload, verify=False)

        res = r.json()

        self.write_customer_card_id(res)

    # 将顾客卡id写入到init表中
    def write_customer_card_id(self, res):
        if isinstance(res['val'], list) and res['val'] != []:
            for i in range(len(res['val'])):
                if res['val'][i]['cardType'] == '1':
                    StartBefore().write_back_init(test_tmp_path, 'init', 2, res['val'][i]['membershipCardId'])
                elif res['val'][i]['cardType'] == '2':
                    StartBefore().write_back_init(test_tmp_path, 'init', 3, res['val'][i]['membershipCardId'])
                elif res['val'][i]['cardType'] == '3':
                    StartBefore().write_back_init(test_tmp_path, 'init', 4, res['val'][i]['membershipCardId'])
                else:
                    logging.info('顾客没有卡')


if __name__ == '__main__':
    start = StartBeforeNew()
    # start.before_test_new_customer()
    start.new_customer_card()
