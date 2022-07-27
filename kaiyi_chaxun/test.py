# m_json = '{"is_admin":"false","pagetemplate_id":107914,"dataset_id":391838,"action":"productitem_web.list","kwargs":{"limit":10,"offset":0,"filters":{"data__name__icontains":"null","data__category_uuid":"%s"},"order_by":["data__saleprice__int"]}}' % '农田'
# print(m_json)
#
# m_json = '{"is_admin":"false","pagetemplate_id":107914,"dataset_id":391838,"action":"productitem_order.submit","kwargs":{"productitem_uuid":"%s"}}' % 'qqqqq-wdddqwd-qq'
# print(m_json)

import execjs
import time
import os
import json
import requests
import keyboard
import datetime

os.environ["EXECJS_RUNTIME"] = "Node"
current_milli_time = lambda: int(round(time.time() * 1000))


def dcoding(m_json, m_time):
    # js_env = execjs.get().name
    res = None
    with open('./c9ed10dc.js') as f:
        ctx = execjs.compile(f.read())
        res = ctx.call("jsstart", m_json, m_time)
    return res

def sm_json():
    # m_json = '{"is_admin":"false","pagetemplate_id":107914,"dataset_id":391838,"action":"order_web.detail","kwargs":{"uuid":"0ff88b6c-3243-493a-98ff-3001bc6056c0"}}'
    m_json = {
    "status":"success",
    "message":"OK",
    "result":{
        "status":"success",
        "object":{
            "id":405474962,
            "is_active":"true",
            "created":"2022-07-26T22:10:23.105351",
            "last_modified":"2022-07-26T22:10:23.105358",
            "company_id":24231,
            "datasettable_id":215482,
            "order":0,
            "uuid":"eac66613-8861-4d10-9f8e-a11461173582",
            "siteuser_id":"null",
            "data":{
                "siteuser_id":2208720,
                "role_uuid":"null",
                "pshop_formdata":{

                },
                "pshop_form":{

                },
                "growth":0,
                "is_certify":"false",
                "certify_date":"1970-01-01T00:00:00.000000",
                "name":"",
                "mobile":"18357630450",
                "id_card":"",
                "front":"placeholder/600x300/DDD/000/default/",
                "back":"placeholder/600x300/DDD/000/default/",
                "birthdate":"1999-12-12T12:00:00.000000",
                "gender":"male",
                "nickname":"",
                "avatar":"placeholder/600x300/DDD/000/default/",
                "credit":0,
                "alipay_name":"",
                "alipay_account":"",
                "alipay_code":"placeholder/600x300/DDD/000/default/",
                "account_name":"",
                "account_bank":"",
                "account_number":"",
                "bgimage":"placeholder/600x300/DDD/000/default/",
                "is_active":"true",
                "pshop_level_uuid":"dacefa7f-21af-44ed-9818-2a1f35bb7d45",
                "is_setpay":"false",
                "paypassword":"",
                "update_date":"1970-01-01T00:00:00.000000",
                "login_time":"2022-07-26T22:10:23.101",
                "sesstion_key":"",
                "is_guide":"false",
                "score":0,
                "pshop_level_uuid__toone":{
                    "id":390916994,
                    "is_active":"true",
                    "created":"2022-04-16T14:21:08.119906",
                    "last_modified":"2022-04-17T11:29:46.026429",
                    "company_id":24231,
                    "datasettable_id":215507,
                    "order":0,
                    "uuid":"dacefa7f-21af-44ed-9818-2a1f35bb7d45",
                    "siteuser_id":"null",
                    "data":{
                        "name":"默认等级",
                        "rate":5,
                        "min_growth":0
                    },
                    "_resource_uri":"db.datasetrow?dataset_id=391838&table_name=pshop_level&id=390916994"
                },
                "siteuser_id__toone":{
                    "id":2208720,
                    "namespace":"default",
                    "site_id":24860,
                    "group_id":"null",
                    "role_id":"null",
                    "content_type_id":81,
                    "object_id":24231,
                    "consumer_id":"null",
                    "weixin_id":"null",
                    "demlution_openid":"null",
                    "name":"null",
                    "completed":"false",
                    "role_verified":"false",
                    "is_active":"true",
                    "is_temp":"false",
                    "is_test":"false",
                    "is_deleted":"false",
                    "created":"2022-07-26T22:08:45.831339",
                    "last_modified":"2022-07-26T22:08:45.850474",
                    "checkin_count":0,
                    "last_checkin":"null",
                    "dshareconfig_id":"null",
                    "dshareconfig_active_url":"null",
                    "dshareconfig_last_modified":"null",
                    "source_type":"mobile",
                    "source_platform":"mobile",
                    "username":"18357630450",
                    "password":"null",
                    "nickname":"null",
                    "email":"null",
                    "email_verified":"false",
                    "mobile":"18357630450",
                    "is_wechat":"false",
                    "avatar":"null",
                    "last_login":"null",
                    "last_login_ip":"null",
                    "signature":"null",
                    "referrer_id":"null",
                    "userrank":"",
                    "pshop_open":"false",
                    "pshop_created":"null",
                    "pshop_state":"created",
                    "pshop_parent_id":"null",
                    "pshop_parent_created":"null",
                    "pshop_money":0,
                    "pshop_withdraw_money":0,
                    "pshop_total_money":0,
                    "pshop_pformdata_id":"null",
                    "pshop_level_id":"null",
                    "cardid":"null",
                    "card_money":"0.00",
                    "money_count":"0.00",
                    "card_status":"normal",
                    "card_created":"null",
                    "wx_cardid":"null",
                    "card_pformdata_id":"null",
                    "branch_id":"null",
                    "user_id":"null",
                    "card_level_id":"null",
                    "card_saler_id":"null",
                    "role_pformdata_id":"",
                    "extra":{

                    },
                    "data":{

                    },
                    "_display_avatar":"static/company/m_ucenter/imgs/usercenter_head.jpg",
                    "_display_pshop_state":"未申请",
                    "_display_nickname":"18357630450",
                    "_hide_mobile_nickname":"183*****450",
                    "_hide_mobile":"183*****450",
                    "_display_source_platform":"手机",
                    "_display_source_type":"手机号注册",
                    "_credits_shop":"0",
                    "_resource_uri":"db.siteuser?id=2208720"
                },
                "benefit":0
            },
            "_resource_uri":"db.datasetrow?dataset_id=391838&table_name=member&id=405474962"
        }
    },
    "logs": ""
    }

    t_json = m_json['result']['object']
    phone = '18357630450'
    ob_id = t_json['id']
    siteuser_id = t_json['data']['siteuser_id']
    # sm_name = 实名姓名
    # id_card = sfz号码
    mobile = phone
    sm_name = '袁野'
    sm_card = '210104198902272838'
    created = t_json['created']
    last_modified = t_json['last_modified']
    username = '{0}'.format(phone)
    pshop_created = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    pshop_parent_created = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    hi_json = t_json['data']['siteuser_id__toone']
    _hide_mobile_nickname = hi_json['_hide_mobile']
    sm_json = '{"is_admin":"false","pagetemplate_id":107914,"dataset_id":391838,"action":"member_web.update_auth","kwargs":{"id":%s,"formData":{"back":"placeholder/600x300/DDD/000/default/","name":"%s","front":"placeholder/600x300/DDD/000/default/","score":0,"avatar":"placeholder/600x300/DDD/000/default/","credit":0,"gender":"male","growth":0,"mobile":"%s","bgimage":"placeholder/600x300/DDD/000/default/","id_card":"%s","is_guide":"false","nickname":"","birthdate":"1999-12-12T12:00:00.000000","is_active":"true","is_setpay":"false","role_uuid":"null","is_certify":"false","pshop_form":{},"alipay_code":"placeholder/600x300/DDD/000/default/","alipay_name":"","siteuser_id":%s,"account_bank":"","account_name":"","account_number":"","alipay_account":"","pshop_formdata":{},"pshop_level_uuid":"dacefa7f-21af-44ed-9818-2a1f35bb7d45","pshop_level_uuid__toone":{"id":390916994,"uuid":"dacefa7f-21af-44ed-9818-2a1f35bb7d45","data":{"name":"默认等级"},"_resource_uri":"db.datasetrow?dataset_id=391838&table_name=pshop_level&id=390916994"},"siteuser_id__toone":{"id":%s,"namespace":"default","site_id":24860,"group_id":"null","role_id":"null","content_type_id":81,"object_id":24231,"consumer_id":"null","weixin_id":"null","demlution_openid":"null","name":"null","completed":"false","role_verified":"false","is_active":"true","is_temp":"false","is_test":"false","is_deleted":"false","created":"%s","last_modified":"%s","checkin_count":0,"last_checkin":"null","dshareconfig_id":"null","dshareconfig_active_url":"null","dshareconfig_last_modified":"null","source_type":"mobile","source_platform":"mobile","username":"%s","password":"null","nickname":"null","email":"null","email_verified":"false","mobile":"%s","is_wechat":"false","avatar":"null","last_login":"null","last_login_ip":"null","signature":"null","referrer_id":"null","userrank":"","pshop_open":"true","pshop_created":"%s","pshop_state":"open","pshop_parent_id":1953726,"pshop_parent_created":"%s","pshop_money":0,"pshop_withdraw_money":0,"pshop_total_money":0,"pshop_pformdata_id":"null","pshop_level_id":"null","cardid":"null","card_money":"0.00","money_count":"0.00","card_status":"normal","card_created":"null","wx_cardid":"null","card_pformdata_id":"null","branch_id":"null","user_id":"null","card_level_id":"null","card_saler_id":"null","role_pformdata_id":"null","extra":{},"data":{},"_display_avatar":"static/company/m_ucenter/imgs/usercenter_head.jpg","_display_pshop_state":"正常运行","_display_nickname":"%s","_hide_mobile_nickname":"%s","_hide_mobile":"%s","_display_source_platform":"手机","_display_source_type":"手机号注册","_credits_shop":"0","_resource_uri":"db.siteuser?id=%s"},"benefit":0}}}' % (
    ob_id, sm_name, phone, sm_card, siteuser_id, siteuser_id, created, last_modified, username, mobile, pshop_created,
    pshop_parent_created, mobile, _hide_mobile_nickname, _hide_mobile_nickname, siteuser_id)
    print(sm_json)


if __name__ == '__main__':
    order_id = '11111'
    uuid = '22222'
    payo_json = '{"is_admin":false,"pagetemplate_id":118729,"dataset_id":393375,"action":"payment.create_moyun_order","kwargs":{"code":"moyun?channel=alipay","order_id":%s,"return_url":"https://m.kai-verse.cn/p/1002588/#/app_kaiyipay-afterpay?order_uuid=%s"}}' % (
    order_id, uuid)
    print(payo_json)
    pass