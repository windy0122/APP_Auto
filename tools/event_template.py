from tools.common import StartBefore
from tools.read_config import ReadConfig
from tools.project_path import *
import requests
import json
import logging
import tools.api_logging

url_conf = ReadConfig().get_config(test_config_path, 'URL', 'url')
url_pfm = ReadConfig().get_config(test_config_path, 'URL', 'url_pfm_uat')


class EventTemplate(object):
    header = {'content-type': 'application/json',
              'version': '1.4.1',
              'platform': 'iOS',
              'tk': StartBefore().get_data_init(6)
              }

    # 创建玫瑰券
    # https://uatleague.round-table-union.com/api/rts/activity/event/createEvent4Shop/V141
    def create_new_event(self):
        url_new_event = url_conf + '/api/rts/activity/event/createEvent4Shop/V141'

        payload = {
            "couponItemDesc": "",
            "couponItemName": "玫瑰券测试",
            "couponItemPreferentialPrice": "1",
            "couponItemPrice": "100",
            "couponPropertyStatus": "2",
            "couponTemplateId": '',
            "couponUseRules": "",
            "couponUseRulesJson": "",
            "couponValidPeriod": "",
            "discountRate": "30",
            "eventId": "",
            "eventImageList": [{
                "eventImageDefaultYn": "",
                "eventImageHeight": "1080",
                "eventImageId": "",
                "eventImageUrl": "https://ossuat.round-table-union.com/349549553790263296/eventImage/zp_029c390448bb5ef451cc692bb8b4a338.jpg",
                "eventImageWidth": "658"
            }],
            "eventTypeId": "5",
            "fastCreateCouponTemplateId": "",
            "fastCreateFlag": "0",
            "itemGroupId": "1",
            "itemGroupName": "剪发"
            }

        r = requests.post(url_new_event, headers=self.header, data=json.dumps(payload), verify=False)

        res = r.json()
        # print(res)

        # rose_coupon_template_id = res['val']['couponTemplateId']
        rose_event_id = res['val']['eventId']
        StartBefore().write_back_init(test_tmp_path, 'init', 11, rose_event_id)
        # return rose_event_id

    # 获取新客券详情
    # https://uatleague.round-table-union.com/api/rts/activity/event/getCouponTemplateWelcome/V124?eventId=508269027298889728
    def get_rose_new_template_detail(self):
        url_rose_new_template_detail = url_conf + '/api/rts/activity/event/getCouponTemplateWelcome/V124'

        payload = {
            'eventId': StartBefore().get_data_init(11)
        }

        r = requests.get(url_rose_new_template_detail, headers=self.header, params=payload, verify=False)

        res = r.json()
        new_coupon_template_id = res['val']['templateWelcomeResponse'][0]['couponTemplateId']
        StartBefore().write_back_init(test_tmp_path, 'init', 12, new_coupon_template_id)

    # 修改活动使用须知
    # https://uatleague.round-table-union.com/api/rts/activity/event/updateEventUseRules/V124
    def update_event_rules(self):
        url_update_event_rules = url_conf + '/api/rts/activity/event/updateEventUseRules/V124'

        payload = {
                "couponUseRules": "[{'key':'有效期','value':['购券后90天内有效']}]",
                "eventId": StartBefore().get_data_init(11),
                "couponUseRulesJson": "{'367016240965775360':{'367016398554165248':{'401765291997036544':{"
                                      "'isSelected':true,'title':'购券后90天内有效','selectedUnavailableDate':'',"
                                      "'selectedExperienceItemsCount':''}}}}",
                "couponTemplateId": StartBefore().get_data_init(12),
                "couponValidPeriod": "90"
            }

        r = requests.post(url_update_event_rules, headers=self.header, data=json.dumps(payload), verify=False)
        # res = r.json()
        # print(res)

    # 提交玫瑰券
    # https://uatleague.round-table-union.com/api/rts/operate/event/apply/submitEvent4Shop/V141
    def submit_rose_event(self):
        url_submit_rose_event = url_conf + '/api/rts/operate/event/apply/submitEvent4Shop/V141'

        payload = {
                "eventId": StartBefore().get_data_init(11),
                "eventType": "5"
            }

        r = requests.post(url_submit_rose_event, headers=self.header, data=json.dumps(payload), verify=False)
        res = r.json()
        if res['msg'] == '操作成功':
            logging.info('提交玫瑰券成功')
        else:
            logging.info('提交玫瑰券失败')

        StartBefore().write_back_init(test_tmp_path, 'init', 13, res['val']['applyId'])

    # 审核玫瑰券(approStatusId为上下架状态，2为下架审核，3为上架审核)
    @staticmethod
    def apply_success(appro_status_id):
        url_apply_success = url_pfm + '/api2/rts/operate/event/apply/appro/V140'

        header = {
            'tk': StartBefore().get_data_init(10),
            'platform': 'Web',
            'version': '1.5.0',
            'Content-Type': 'application/json;charset=UTF-8'
        }

        payload = {
                "applyId": StartBefore().get_data_init(13),
                "approRemark": "测试",
                "approStatusId": appro_status_id
            }

        r = requests.post(url_apply_success, headers=header, data=json.dumps(payload), verify=False)
        res = r.json()
        if res['msg'] == '操作成功':
            logging.info('玫瑰券上架成功')
        else:
            logging.info('玫瑰券上架失败')
        # print(res)

    # 提交下架玫瑰券申请
    def off_shelf(self):
        url_off_shelf = '/api/rts/operate/event/apply/lowershelf4Shop/add/V141'

        payload = {
            'eventId': StartBefore().get_data_init(11)
        }

        r = requests.get(url_off_shelf, headers=self.header, params=json.dumps(payload), verify=False)
        res = r.json()
        if res['msg'] == '操作成功':
            logging.info('提交玫瑰券下架申请成功')
        else:
            logging.info('提交玫瑰券下架申请失败')


if __name__ == '__main__':
    event = EventTemplate()
    event.create_new_event()
    event.get_rose_new_template_detail()
    event.update_event_rules()
    event.submit_rose_event()
    event.apply_success(3)






