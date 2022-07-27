import execjs
import time
import os
import json
import requests
import keyboard

from config import global_config
from timer import Timer
from logger import logger

timer = Timer()

os.environ["EXECJS_RUNTIME"] = "Node"
current_milli_time = lambda: int(round(time.time() * 1000))

class KaiYi(object):
    def __init__(self):
        self.session = requests.Session()
        self.phone = global_config.getRaw('user','user_phone')
        self.password = global_config.getRaw('user','user_pd')
        self.mark_list = dict()
        self.price_list = dict()
        self.mark_list['农田'] = '2af87a8d-673a-40af-9d79-1db14f1a5f7e'
        self.price_list['农田'] = 100
        self.mark_list['豹1'] = '3a14d5cc-dab7-4338-b2ea-3b56cacccfe4'
        self.price_list['豹1'] = 1000
        self.mark_list['平1'] = '7bd57e94-8910-4723-8e33-2943fb480867'
        self.price_list['平1'] = 10000
        self.mark_list['平2'] = '4aa81d90-b4d9-4447-8940-ac8147275bdd'
        self.price_list['平2'] = 2000


    def dcoding(self, m_json, m_time):
        # js_env = execjs.get().name
        res = None
        with open('./c9ed10dc.js') as f:
            ctx = execjs.compile(f.read())
            res = ctx.call("jsstart", m_json, m_time)
        return res

    def login(self):
        headers = {
            'Host': 'm.kaione-sh.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'X-Log-Cnickname': 'kywh',
            'X-Log-Pid': '987827',
            'X-Log-Lhash': '#/app_kaiyi-pshopsharetarget',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://m.kaione-sh.cn',
            'Referer': 'https://m.kaione-sh.cn/',
        }
        login_url = 'https://m.kaione-sh.cn/capi/v1/company_account/login'
        login_json = {
            "username": "{0}".format(self.phone),
            "password": "{0}".format(self.password)
        }

        for l in range(3):
            try:
                res = self.session.post(login_url, headers=headers, json=login_json, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['message_type'] == 'login_success' or m_json['message'] == '登陆成功':
                        logger.info("登录成功----%s----%s", self.phone, self.password)
                        break
                with open("./login_error.txt", "a") as file:
                    file.write(self.phone + '----' + self.password + '\n')
            except Exception as e:
                logger.info(e)

    def a_pay_order(self):
        a_pay_url = 'https://m.kaione-sh.cn/dapi/ccode/run?papp_slug=kaiyi&action=member_web.get_create_member&pagetemplate_id=107914&dataset_id=391838'
        dc_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"member_web.get_create_member","kwargs":{}}'

        for nn in range(3):
            try:
                m_time = current_milli_time()
                data = self.dcoding(dc_json, m_time)
                headers = {
                    'Host': 'm.kaione-sh.cn',
                    'Connection': 'keep-alive',
                    'X-Request-Timestamp': '{0}'.format(m_time),
                    'X-Log-Cnickname': 'kywh',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'X-Log-Pid': '987827',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://m.kaione-sh.cn',
                    'Referer': 'https://m.kaione-sh.cn/'
                }
                res = self.session.post(a_pay_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    break

            except Exception as e:
                print(e)

    def pay_order(self, uuid):
        pay_url = 'https://m.kaione-sh.cn/dapi/ccode/run?papp_slug=kaiyi&action=order_user.submit_credit_pay&pagetemplate_id=107914&dataset_id=391838'
        dc_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"order_user.submit_credit_pay","kwargs":{"order_uuid":"%s","paypassword":""}}' % uuid
        # self.a_pay_order()

        for nn in range(3):
            try:
                m_time = current_milli_time()
                data = self.dcoding(dc_json, m_time)
                headers = {
                    'Host': 'm.kaione-sh.cn',
                    'Connection': 'keep-alive',
                    'X-Request-Timestamp': '{0}'.format(m_time),
                    'X-Log-Cnickname': 'kywh',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'X-Log-Lhash': '#/app_kaiyi-payment?order_uuid={0}'.format(uuid),
                    'X-Log-Pid': '987827',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://m.kaione-sh.cn',
                    'Referer': 'https://m.kaione-sh.cn/'
                }
                res = self.session.post(pay_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['status'] == 'success' and m_json['message'] == 'OK' and m_json['result']['status'] == 'success':
                        logger.info('购买成功')
                        self.check_order(uuid)
                        break
            except Exception as e:
                print(e)

    def check_order(self, uuid):
        dc_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"order_web.detail","kwargs":{"uuid":"%s"}}' % uuid
        check_url = 'https://m.kaione-sh.cn/dapi/ccode/run?papp_slug=kaiyi&action=order_web.detail&pagetemplate_id=107914&dataset_id=391838'

        for nn in range(3):
            try:
                m_time = current_milli_time()
                data = self.dcoding(dc_json, m_time)
                headers = {
                    'Host': 'm.kaione-sh.cn',
                    'Connection': 'keep-alive',
                    'X-Request-Timestamp': '{0}'.format(m_time),
                    'X-Log-Cnickname': 'kywh',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'X-Log-Lhash': '#/app_kaiyi-payment?order_uuid={0}'.format(uuid),
                    'X-Log-Pid': '987827',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://m.kaione-sh.cn',
                    'Referer': 'https://m.kaione-sh.cn/'
                }
                res = self.session.post(check_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['status'] == 'success' and m_json['message'] == 'OK':
                        t_json = m_json['result']['object']
                        logger.info('商品名: %s, 购买价格: %s, 商品链接: https://m.kaione-sh.cn/#/app_kaiyi-productitemdetail?productitem_uuid=%s, 付款时间: %s' % (t_json['data']['version'], t_json['data']['price'], t_json['data']['productitem_uuid'], t_json['data']['endTime']))
                        break
            except Exception as e:
                print(e)


    def create_order(self, uuid):
        c_order_url = 'https://m.kaione-sh.cn/dapi/ccode/run?papp_slug=kaiyi&action=productitem_order.submit&pagetemplate_id=107914&dataset_id=391838'
        dc_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"productitem_order.submit","kwargs":{"productitem_uuid":"%s"}}' % uuid

        for nn in range(3):
            try:
                m_time = current_milli_time()
                data = self.dcoding(dc_json, m_time)
                headers = {
                    'Host': 'm.kaione-sh.cn',
                    'Connection': 'keep-alive',
                    'X-Request-Timestamp': '{0}'.format(m_time),
                    'X-Log-Cnickname': 'kywh',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'X-Log-Lhash': '#/app_kaiyi-productitemlist',
                    'X-Log-Pid': '987827',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://m.kaione-sh.cn',
                    'Referer': 'https://m.kaione-sh.cn/'
                }
                res = self.session.post(c_order_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['status'] == 'success' and m_json['message'] == 'OK':
                        if m_json['result']['status'] == 'success':
                            logger.info("锁单成功")
                            t_json = m_json['result']['order']
                            self.pay_order(t_json['uuid'])
                            break
                        elif m_json['result']['status'] == 'error' and m_json['result']['message'] == '存在未支付订单，请前往支付或取消该订单！':
                            print('存在未支付订单')
                            time.sleep(60)
                        elif m_json['result']['status'] == 'error' and m_json['result']['message'] == '您的原石余额不足 不能下单 ':
                            print('余额不足')
                            time.sleep(60)
                        else:
                            pass
            except Exception as e:
                print(e)



    def seckill_low(self, m_pro):
        mark_url = 'https://m.kaione-sh.cn/dapi/ccode/run?papp_slug=kaiyi&action=productitem_web.list&pagetemplate_id=107914&dataset_id=391838'
        print('等待alt+r')
        # keyboard.wait('alt+r')
        print('alt+r')
        time.sleep(2)

        while True:
            print('抄底中----{0}'.format(m_pro))
            m_time = current_milli_time()
            dc_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"productitem_web.list","kwargs":{"limit":10,"offset":0,"filters":{"data__name__icontains":null,"data__category_uuid":"%s"},"order_by":["data__saleprice__int"]}}' % self.mark_list[m_pro]
            data = self.dcoding(dc_json, m_time)
            headers = {
                'Host': 'm.kaione-sh.cn',
                'Connection': 'keep-alive',
                'X-Request-Timestamp': '{0}'.format(m_time),
                'X-Log-Cnickname': 'kywh',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                'X-Log-Lhash': '#/app_kaiyi-productitemlist',
                'X-Log-Pid': '987827',
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://m.kaione-sh.cn',
                'Referer': 'https://m.kaione-sh.cn/'
            }

            try:
                res = self.session.post(mark_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['status'] == 'success' and m_json['message'] == 'OK':
                        t_json = m_json['result']['objects']
                        t_data = t_json[0]['data']
                        if t_data['saleprice'] <= self.price_list[m_pro]:
                            t_uuid = t_json[0]['uuid']
                            self.create_order(t_uuid)
                            time.sleep(0.5)
                            return
                time.sleep(5)
            except Exception as e:
                print(e)


Ky = KaiYi()