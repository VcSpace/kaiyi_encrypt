import execjs
import time
import os
import json
import requests
import keyboard
import datetime
import random
import selenium.webdriver.support.ui as ui

from config import global_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from logger import logger


os.environ["EXECJS_RUNTIME"] = "Node"
current_milli_time = lambda: int(round(time.time() * 1000))

class KaiYi(object):
    def __init__(self):

        self.login_session = requests.Session()


    def dcoding(self, m_json, m_time):
        # js_env = execjs.get().name
        res = None
        with open('./c9ed10dc.js') as f:
            ctx = execjs.compile(f.read())
            res = ctx.call("jsstart", m_json, m_time)
        return res

    def store_login(self, phone, password):
        self.use_flag = False
        self.session = requests.Session()
        store_url = 'https://m.kai-verse.cn/capi/v1/company_account/login'
        headers = {
            'Host': 'm.kai-verse.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://m.kai-verse.cn',
            'Referer': 'https://m.kai-verse.cn/p/1002588/'
        }

        store_json = {
            "username":"{0}".format(phone),
            "password":"{0}".format(password)
        }
        for send in range(3):
            try:
                res = self.session.post(store_url, headers=headers, json=store_json, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['message_type'] == 'password_not_match_account':
                        self.tmp_driver_login(phone, password)
                        continue
                    if m_json['message_type'] == 'login_success' and m_json['message'] == '登录成功！':
                        logger.info('商店登陆成功 %s' %phone)
                        break
                    elif m_json['result']['message'] == '用户未登录！':
                        self.tmp_driver_login(phone, password)
                        continue
                    else:
                        self.tmp_driver_login(phone, password)
                        time.sleep(5)
            except Exception as e:
                time.sleep(60)
                logger.info(e)

    def five_pay(self):
        five_url = 'https://m.kai-verse.cn/dapi/ccode/run?papp_slug=kaiyipay&action=product_order.submit&pagetemplate_id=118729&dataset_id=393375'
        five_json = '{"is_admin":false,"pagetemplate_id":118729,"dataset_id":393375,"action":"product_order.submit","kwargs":{"product_uuid":"5d577893-35ca-4508-90e4-ac7f86001d28"}}'

        for nn in range(3):
            try:
                m_time = current_milli_time()
                data = self.dcoding(five_json, m_time)
                headers = {
                    'Host': 'm.kai-verse.cn',
                    'Connection': 'keep-alive',
                    'X-Request-Timestamp': '{0}'.format(m_time),
                    'X-Log-Cnickname': 'kywh',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'X-Log-Pid': '987827',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://m.kai-verse.cn',
                    'Referer': 'https://m.kai-verse.cn/p/1002588/'
                }
                res = self.session.post(five_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    t_json = m_json['result']['order']
                    logger.info("创建订单成功")
                    return t_json['uuid']
            except Exception as e:
                print(e)

    def create_order(self, uuid):
        order_json = '{"is_admin":false,"pagetemplate_id":118729,"dataset_id":393375,"action":"order_web.detail","kwargs":{"uuid":"%s"}}' % uuid
        create_url = 'https://m.kai-verse.cn/dapi/ccode/run?papp_slug=kaiyipay&action=order_web.detail&pagetemplate_id=118729&dataset_id=393375'
        for nn in range(3):
            try:
                m_time = current_milli_time()
                data = self.dcoding(order_json, m_time)
                headers = {
                    'Host': 'm.kai-verse.cn',
                    'Connection': 'keep-alive',
                    'X-Request-Timestamp': '{0}'.format(m_time),
                    'X-Log-Cnickname': 'kywh',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'X-Log-Pid': '987827',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://m.kai-verse.cn',
                    'Referer': 'https://m.kai-verse.cn/p/1002588/'
                }
                res = self.session.post(create_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    t_json = m_json['result']['object']
                    logger.info("创建订单成功")
                    return t_json['data']['order_id']

            except Exception as e:
                print(e)

    def pay_order(self, uuid, order_id):#原石
        payo_json = '{"is_admin":false,"pagetemplate_id":118729,"dataset_id":393375,"action":"payment.create_moyun_order","kwargs":{"code":"moyun?channel=alipay","order_id":%s,"return_url":"https://m.kai-verse.cn/p/1002588/#/app_kaiyipay-afterpay?order_uuid=%s"}}' % (order_id,uuid)
        payo_url = 'https://m.kai-verse.cn/dapi/ccode/run?papp_slug=kaiyipay&action=payment.create_moyun_order&pagetemplate_id=118729&dataset_id=393375'
        for nn in range(3):
            try:
                m_time = current_milli_time()
                data = self.dcoding(payo_json, m_time)
                headers = {
                    'Host': 'm.kai-verse.cn',
                    'Connection': 'keep-alive',
                    'X-Request-Timestamp': '{0}'.format(m_time),
                    'X-Log-Cnickname': 'kywh',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'X-Log-Pid': '987827',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://m.kai-verse.cn',
                    'Referer': 'https://m.kai-verse.cn/p/1002588/'
                }
                res = self.session.post(payo_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    return 'https://m.kai-verse.cn/' + m_json['result']['pay_url']
            except Exception as e:
                print(e)

    def check_order(self, uuid):
        status_json = '{"is_admin":false,"pagetemplate_id":118729,"dataset_id":393375,"action":"order_web.detail","kwargs":{"uuid":"%s"}}' % uuid
        status_url = 'https://m.kai-verse.cn/dapi/ccode/run?papp_slug=kaiyipay&action=order_web.detail&pagetemplate_id=118729&dataset_id=393375'

        while True:
            try:
                m_time = current_milli_time()
                data = self.dcoding(status_json, m_time)
                headers = {
                    'Host': 'm.kai-verse.cn',
                    'Connection': 'keep-alive',
                    'X-Request-Timestamp': '{0}'.format(m_time),
                    'X-Log-Cnickname': 'kywh',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'X-Log-Pid': '987827',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://m.kai-verse.cn',
                    'Referer': 'https://m.kai-verse.cn/p/1002588/'
                }
                res = self.session.post(status_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    t_json = m_json['result']['object']
                    if t_json['data']['remark'] == '已正常发货':
                        self.buy_tianyuan()
                        break
                    else:
                        time.sleep(5)
                        continue
            except Exception as e:
                print(e)


    def login(self, phone, password, uuid, pay_url):
        self.driver_login(phone, password, pay_url)
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
            "username": "{0}".format(phone),
            "password": "{0}".format(password)
        }

        for l in range(3):
            try:
                res = self.login_session.post(login_url, headers=headers, json=login_json, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['message_type'] == 'login_success' or m_json['message'] == '登陆成功':
                        logger.info("登录成功----%s----%s", phone, password)
                        self.check_order(uuid)
                        break
                with open("./pay_login_error.txt", "a") as file:
                    file.write(phone + '----' + password + '\n')
            except Exception as e:
                logger.info(e)

    def get_ip(self):
        ipurl = 'http://api1.ydaili.cn/tools/BMeasureApi.ashx?action=BEAPI&secret=B29A8906A8B75EFD7485C8B5A77E30DEA2A1FD0DB3F5E262&number=1&orderId=34550&format=json'
        req = requests.get(ipurl)
        tjson = json.loads(req.text)
        if tjson['status'] == 'success':
            get_ip = tjson['data'][0]
            ip = get_ip['IP']
            return ip

    def tmp_driver_login(self, phone, password):
        options = webdriver.ChromeOptions()
        # 无痕模式
        options.add_argument('--incognito')
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

        # 启动chrome浏览器无痕模式
        driver = webdriver.Chrome(chrome_options=options)
        # driver.set_window_size(550, 820)
        x1 = 0
        x2 = 350
        x3 = 650
        x4 = 950
        x5 = 1200

        driver.set_window_rect(x=x3, y=0, height=820, width=350)

        driver.get('http://www.baidu.com')  # 打开url网页 比如 driver.get("http://www.baidu.com")
        time.sleep(0)
        # login_url = 'https://m.kaione-sh.cn/#/app_kaiyi-login'
        uid = global_config.getRaw('user', 'user_uid')
        js = "window.open('https://m.kaione-sh.cn/?pshop_id={0}#/app_kaiyi-pshopsharetarget','_blank');".format(uid)
        # js = "window.open('https://m.kaione-sh.cn/#/app_kaiyi-homepage?member_uuid=353c1df4-bcbd-425e-9352-e1715ad0a53b','_blank');" #我
        try:
            wait = ui.WebDriverWait(driver, 10)
            driver.execute_script(js)
            list_windows = driver.window_handles
            driver.switch_to.window(list_windows[1])
            wait.until(lambda driver: driver.find_element_by_css_selector('.id_7cc5cd2b9704f1115426696c .b-input'))
            driver.find_element_by_css_selector('.id_7cc5cd2b9704f1115426696c .b-input').send_keys(phone)
            time.sleep(0.2)
            wait.until(lambda driver: driver.find_element_by_css_selector('.id_f2a17f453a6f686ee18bed14 .b-input'))
            driver.find_element_by_css_selector('.id_f2a17f453a6f686ee18bed14 .b-input').send_keys(password)
            sign_cho = '#vue-view > section.s-dwvapp-slide-container > div > div.van-pull-refresh > div > section > section.s-dwvapp-component.id_d5242e838b5ae0b2af67b8df > section > section > section.s-vbench-container.a-dlayout-type-dom > section > section > section:nth-child(1) > section.dlayout-bag.s-vbench-bag-if-true > section:nth-child(2) > section.dlayout-bag.s-vbench-bag-if-true > section > section.dlayout-bag > section:nth-child(1) > section.dlayout-bag.s-vbench-bag-if-true > section > section.dlayout-bag > section > section.dlayout-bag > section > section.dlayout-bag > section:nth-child(6) > section.dlayout-bag > section.dlayout-item.slide-type-dwapp_cloud > section.dlayout-item-container > section > section > div > div > div > div > div > div > div > label > label > i'
            wait.until(lambda driver: driver.find_element_by_css_selector(sign_cho))
            js = driver.find_element_by_css_selector(sign_cho)
            driver.execute_script("arguments[0].click();", js)
            que_but = '.van-dialog__confirm, .van-dialog__confirm:active'
            wait.until(lambda driver: driver.find_element_by_css_selector(que_but))
            js = driver.find_element_by_css_selector(que_but)
            driver.execute_script("arguments[0].click();", js)
            wait.until(
                lambda driver: driver.find_element_by_css_selector('.id_a5852a4c8f7eaa70dc9e9087 .b-button.b-group-text1'))
            driver.find_element_by_css_selector('.id_a5852a4c8f7eaa70dc9e9087 .b-button.b-group-text1').click()
            self.use_flag = True
            keyboard.wait('alt+r')
            print('alt+r')
        except Exception as e:
            self.use_flag = True
            keyboard.wait('alt+r')
            print('alt+r')


    def driver_login(self, phone, password, pay_url):
        options = webdriver.ChromeOptions()
        # 无痕模式
        options.add_argument('--incognito')
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

        # 启动chrome浏览器无痕模式
        driver = webdriver.Chrome(chrome_options=options)
        # driver.set_window_size(550, 820)
        x1 = 0
        x2 = 350
        x3 = 650
        x4 = 950
        x5 = 1200

        driver.set_window_rect(x=x3, y=0, height=820, width=350)

        driver.get(pay_url)  # 打开url网页 比如 driver.get("http://www.baidu.com")
        time.sleep(12)
        # login_url = 'https://m.kaione-sh.cn/#/app_kaiyi-login'
        uid = global_config.getRaw('user', 'user_uid')
        js = "window.open('https://m.kaione-sh.cn/?pshop_id={0}#/app_kaiyi-pshopsharetarget','_blank');".format(uid)
        # js = "window.open('https://m.kaione-sh.cn/#/app_kaiyi-homepage?member_uuid=353c1df4-bcbd-425e-9352-e1715ad0a53b','_blank');" #我

        try:
            wait = ui.WebDriverWait(driver, 10)
            driver.execute_script(js)
            list_windows = driver.window_handles
            driver.switch_to.window(list_windows[1])
            wait.until(lambda driver: driver.find_element_by_css_selector('.id_7cc5cd2b9704f1115426696c .b-input'))
            driver.find_element_by_css_selector('.id_7cc5cd2b9704f1115426696c .b-input').send_keys(phone)
            time.sleep(0.2)
            wait.until(lambda driver: driver.find_element_by_css_selector('.id_f2a17f453a6f686ee18bed14 .b-input'))
            driver.find_element_by_css_selector('.id_f2a17f453a6f686ee18bed14 .b-input').send_keys(password)
            sign_cho = '#vue-view > section.s-dwvapp-slide-container > div > div.van-pull-refresh > div > section > section.s-dwvapp-component.id_d5242e838b5ae0b2af67b8df > section > section > section.s-vbench-container.a-dlayout-type-dom > section > section > section:nth-child(1) > section.dlayout-bag.s-vbench-bag-if-true > section:nth-child(2) > section.dlayout-bag.s-vbench-bag-if-true > section > section.dlayout-bag > section:nth-child(1) > section.dlayout-bag.s-vbench-bag-if-true > section > section.dlayout-bag > section > section.dlayout-bag > section > section.dlayout-bag > section:nth-child(6) > section.dlayout-bag > section.dlayout-item.slide-type-dwapp_cloud > section.dlayout-item-container > section > section > div > div > div > div > div > div > div > label > label > i'
            wait.until(lambda driver: driver.find_element_by_css_selector(sign_cho))
            js = driver.find_element_by_css_selector(sign_cho)
            driver.execute_script("arguments[0].click();", js)
            que_but = '.van-dialog__confirm, .van-dialog__confirm:active'
            wait.until(lambda driver: driver.find_element_by_css_selector(que_but))
            js = driver.find_element_by_css_selector(que_but)
            driver.execute_script("arguments[0].click();", js)
            wait.until(
                lambda driver: driver.find_element_by_css_selector('.id_a5852a4c8f7eaa70dc9e9087 .b-button.b-group-text1'))
            driver.find_element_by_css_selector('.id_a5852a4c8f7eaa70dc9e9087 .b-button.b-group-text1').click()
            if self.use_flag == False:
                keyboard.wait('alt+r')
                print('alt+r')
        except Exception as e:
            if self.use_flag == False:
                keyboard.wait('alt+r')
                print('alt+r')



    def buy_tianyuan(self):
        yuan_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"product_order.submit","kwargs":{"product_uuid":"616d48c7-2a5f-42d3-bdbd-d0b05e427530","coupon_item_uuid":null}}'
        yuan_url = 'https://m.kaione-sh.cn/dapi/ccode/run?papp_slug=kaiyi&action=product_order.submit&pagetemplate_id=107914&dataset_id=391838'

        for ll in range(3):
            try:
                m_time = current_milli_time()
                data = self.dcoding(yuan_json, m_time)
                headers = {
                    'Host': 'm.kaione-sh.cn',
                    'Connection': 'keep-alive',
                    'X-Request-Timestamp': '{0}'.format(m_time),
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'X-Log-Cnickname': 'kywh',
                    'X-Log-Pid': '987827',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://m.kaione-sh.cn',
                    'Referer': 'https://m.kaione-sh.cn/',
                }
                res = self.login_session.post(yuan_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['result']['status'] == 'success':
                        t_json = m_json['result']['order']
                        self.yuan_pay_order(t_json['uuid'])
                        break
                    elif m_json['result']['status'] == 'error' and m_json['result'][
                        'message'] == '存在未支付订单，请前往支付或取消该订单！':
                        print('存在未支付订单')
                        time.sleep(6)
                    elif m_json['result']['status'] == 'error' and m_json['result']['message'] == '您的原石余额不足 不能下单 ':
                        print('余额不足')
                        time.sleep(6)
                    else:
                        pass
            except Exception as e:
                print(e)


    def yuan_pay_order(self, uuid):
        yuan_pay = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"order_user.submit_credit_pay","kwargs":{"order_uuid":"%s","paypassword":""}}' % uuid
        yuan_pay_url = 'https://m.kaione-sh.cn/dapi/ccode/run?papp_slug=kaiyi&action=order_user.submit_credit_pay&pagetemplate_id=107914&dataset_id=391838'
        for nn in range(3):
            try:
                m_time = current_milli_time()
                data = self.dcoding(yuan_pay, m_time)
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
                res = self.login_session.post(yuan_pay_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['status'] == 'success' and m_json['message'] == 'OK' and m_json['result']['status'] == 'success':
                        logger.info('购买成功')
                        break
            except Exception as e:
                print(e)


Ky = KaiYi()