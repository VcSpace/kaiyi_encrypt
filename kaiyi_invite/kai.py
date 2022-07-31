import execjs
import time
import os
import json
import requests
import keyboard
import datetime
import random
import threading

from config import global_config
from timer import Timer
from logger import logger
from jm import JM

timer = Timer()


os.environ["EXECJS_RUNTIME"] = "Node"
current_milli_time = lambda: int(round(time.time() * 1000))

class KaiYi(object):
    def __init__(self):
        self.session = requests.Session()
        self.phone = global_config.getRaw('user','user_phone')
        self.password = global_config.getRaw('user','user_pd')
        self.uid = global_config.getRaw('user','user_pd')
        self.cho = global_config.getRaw('jm', 'platform')
        JM.init_jm(self.cho)
        self.threadLock = threading.Lock()
        self.n = '1'


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

    def get_ip(self):
        ipurl = 'http://api1.ydaili.cn/tools/BMeasureApi.ashx?action=BEAPI&secret=B29A8906A8B75EFD7485C8B5A77E30DEA2A1FD0DB3F5E262&number=1&orderId=34550&format=json'
        req = requests.get(ipurl)
        tjson = json.loads(req.text)
        if tjson['status'] == 'success':
            get_ip = tjson['data'][0]
            ip = get_ip['IP']
            return ip

    def ex_olduser(self, phone):
        ex_url = 'https://m.kaione-sh.cn/capi/v1/company_account/signup_with_mobile'
        headers = {
            'Host': 'm.kaione-sh.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'X-Log-Lhash': '#/app_kaiyi-pshopsharetarget',
            'X-Log-Pid': '987827',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://m.kaione-sh.cn',
            'Referer': 'https://m.kaione-sh.cn/?pshop_id={0}'.format(self.uid),
        }
        ex_json = {
            "mobile":"{0}".format(phone),
            "code":"333111",
            "password1":"Kyzxz456123",
            "password2":"Kyzxz456123",
            "invitation_code":""
        }
        try:
            res = requests.post(ex_url, headers=headers, json=ex_json, timeout=60)
            if res.status_code == 200:
                m_json = json.loads(res.text)
                logger.info("%s ----%s", res.text, phone)
                if m_json['message_type'] == 'siteuser_already_registered' and m_json['status'] == 'error' or m_json['message'] == '\u8be5\u624b\u673a\u53f7\u5df2\u7ecf\u6ce8\u518c\uff0c\u8bf7\u76f4\u63a5\u767b\u5f55':
                    return False
                elif m_json['message_type'] == 'verificationcode_error' and m_json['message'] == '\u9a8c\u8bc1\u7801\u9519\u8bef':
                    return True
                else:
                    time.sleep(5)
                    return False
        except Exception as e:
            logger.info(e)


    def invite(self):
        for ll in range(1):
            ip= self.get_ip()
            print(ip)
            self.proxies = {
                "http": "http://{0}".format(ip),
                "https": "http://{0}".format(ip),
            }
            url = "http://www.baidu.com/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
            try:
                response = requests.get(url, headers=headers, proxies=self.proxies, timeout=3)
                print('ip成功')
            except Exception as e:
                print(f"请求失败，代理IP无效！{e}")
                continue


            flag = None
            phone = JM.get_phone(self.cho)
            flag = self.ex_olduser(phone)
            if flag == True:
                get_flag = self.sendmessage(phone)
                if get_flag == False:
                    JM.detail_phone(self.cho, phone)
                    continue
                m_code = JM.get_message(self.cho, phone)
                if m_code == None:
                    continue
                self.reg_user(phone, m_code)
                flag = self.login_user(phone)
                if flag == False:
                    continue
                # self.user_con_inv(phone)
                self.set_userinfo()
                self.user_sm(phone)
                self.logout()
                # self.set_userinfo()
                # self.set_mark_password()
                time.sleep(1)
            else:
                JM.detail_phone(self.cho, phone)
                time.sleep(2)

    def set_userinfo(self):
        self.n = int(self.n) + 1
        self.n = str(self.n)

        headers = {
            'Host': 'm.kaione-sh.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'X-Log-Cnickname': 'kywh',
            'X-Log-Pid': '987827',
            'X-Log-Lhash': '#/app_kaiyi-pshopsharetarget',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://m.kaione-sh.cn',
            'Referer': 'https://m.kaione-sh.cn/',
        }
        randomlength = 16
        user_url = 'https://m.kaione-sh.cn/dapi/psiteuser/set_userinfo'
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        rn = random.randint(5,9)
        for ll in range(rn):
            random_str += base_str[random.randint(0, length)]

        imgarr = ['u/kywh/2022/06/04/kAkHFHVLwoKnkCbCk5NMjN/00000kk.jpg', 'u/kywh/2022/06/04/c43uMsntg86hvdFeTnqqR3/00dqillll.jpg', 'u/kywh/2022/06/04/Vb3Up2bxJhxCrp9KcuSNhC/00kkkooom.jpg', 'u/kywh/2022/06/04/jGdjb5jKAh2DRx3jyEDuxi/00qqqqaaa.jpg', 'u/kywh/2022/06/04/cYoa7KPRkjAFHpn8vBEdAC/00qqqqff.jpg', 'u/kywh/2022/06/04/AJJSkjHdvTVQQ6GozVV5y4/00qqqqqqw.jpg', 'u/kywh/2022/06/04/mBeRdGZyPLGXBpzoRTDdBA/000012.jpg', 'u/kywh/2022/06/04/5qU4CeGtWLTy4CqohoANba/000001234.jpg']
        img_path = imgarr[random.randint(0,7)]
        user_json = {
            "avatar": "{0}".format(img_path),
            "nickname":"{0}".format(random_str + self.n)
        }

        for l in range(3):
            try:
                res = self.session.post(user_url, headers=headers, json=user_json, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['status'] == 'success' or m_json['message'] == '用户信息设置成功':
                        logger.info("用户资料设置成功")
                        break
            except Exception as e:
                logger.info(e)


    def sendmessage(self, phone):
        send_url = 'https://m.kaione-sh.cn/dapi/verification_code/send_verify_code'
        send_json = {
            "mobile":"{0}".format(str(phone))
        }
        headers = {
            'Host': 'm.kaione-sh.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://m.kaione-sh.cn'
        }
        print(send_json)
        for send in range(5):
            try:
                res = self.session.post(send_url, headers=headers, json=send_json, timeout=60)
                if res.status_code == 200:
                    m_json = json.loads(res.text)
                    if m_json['status'] == 'success':
                        print('短信发送成功----', phone)
                        return True
                    else:
                        print("短信发送失败正在重试----%d次" %send)
                        time.sleep(3)
            except Exception as e:
                logger.info(e)
        return False

    def reg_user(self, phone, m_code):
        reg_url = 'https://m.kaione-sh.cn/capi/v1/company_account/signup_with_mobile'
        headers = {
            'Host': 'm.kaione-sh.cn',
            'Connection': 'keep-alive',
            'X-Log-Cnickname': 'kywh',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'X-Log-Lhash': '#/app_kaiyi-pshopsharetarget',
            'X-Log-Pid': '987827',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://m.kaione-sh.cn',
            'Referer': 'https://m.kaione-sh.cn/?pshop_id={0}'.format(self.uid)
        }

        reg_json = {
            "mobile":"{0}".format(phone),
            "code":"{0}".format(m_code),
            "password1":"{0}".format(self.password),
            "password2":"{0}".format(self.password),
            "invitation_code":""
        }

        for l in range(3):
            try:
                res = self.session.post(reg_url, headers=headers, json=reg_json, proxies=self.proxies,timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['message'] == '\u767b\u5f55\u6210\u529f\uff01' and m_json['message_type'] == 'login_success':
                        logger.info('注册成功 %s' % phone)
                        with open("./14_reguser.txt", "a") as file:
                            file.write(phone + '----' + self.password + '\n')
                        return True
            except Exception as e:
                logger.info(e)
        with open("account/reg_error.txt", "a") as file:
            file.write(phone + '----' + self.password + '\n')

    def login_user(self, phone):
        login_url = 'https://m.kaione-sh.cn/capi/v1/company_account/login'
        headers = {
            'Host': 'm.kaione-sh.cn',
            'Connection': 'keep-alive',
            'X-Log-Cnickname': 'kywh',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'X-Log-Lhash': '#/app_kaiyi-pshopsharetarget',
            'X-Log-Pid': '987827',
            'Origin': 'https://m.kaione-sh.cn',
            'Referer': 'https://m.kaione-sh.cn/?pshop_id={0}'.format(self.uid),
        }
        login_json = {
            "username":"{0}".format(phone),
            "password":"{0}".format(self.password)
        }
        for l in range(3):
            try:
                res = self.session.post(login_url, headers=headers, json=login_json,timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['message'] == '登录成功！' and m_json['message_type'] == 'login_success':
                        logger.info('登录成功 %s' % phone)
                        return True
                    elif m_json['message'] == '账号与密码不匹配':
                        return False
            except Exception as e:
                logger.info(e)
        with open("account/reg_error.txt", "a") as file:
            file.write(phone + '----' + self.password + '\n')


    def re_user_sm(self, phone):
        re_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"member_web.get_create_member","kwargs":{}}'
        re_sm_url = 'https://m.kaione-sh.cn/dapi/ccode/run?papp_slug=kaiyi&action=member_web.get_create_member&pagetemplate_id=107914&dataset_id=391838'

        ob_id = None
        for nn in range(3):
            try:
                m_time = current_milli_time()
                data = self.dcoding(re_json, m_time)
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
                res = self.session.post(re_sm_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    t_json = m_json['result']['object']
                    ob_id = t_json['id']
                    siteuser_id = t_json['data']['siteuser_id']
                    try:
                        self.threadLock.acquire()
                        sm_name, sm_card = JM.get_sm()
                        self.threadLock.release()
                    except Exception as e:
                        self.threadLock.release()
                    mobile = phone
                    created = t_json['created']
                    last_modified = t_json['last_modified']
                    username = '{0}'.format(phone)
                    pshop_created = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
                    pshop_parent_created = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
                    hi_json = t_json['data']['siteuser_id__toone']
                    _hide_mobile_nickname = hi_json['_hide_mobile']
                    sm_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"member_web.update_auth","kwargs":{"id":%s,"formData":{"back":"placeholder/600x300/DDD/000/default/","name":"%s","front":"placeholder/600x300/DDD/000/default/","score":0,"avatar":"placeholder/600x300/DDD/000/default/","credit":0,"gender":"male","growth":0,"mobile":"%s","bgimage":"placeholder/600x300/DDD/000/default/","id_card":"%s","is_guide":false,"nickname":"","birthdate":"1999-12-12T12:00:00.000000","is_active":true,"is_setpay":false,"role_uuid":null,"is_certify":false,"pshop_form":{},"alipay_code":"placeholder/600x300/DDD/000/default/","alipay_name":"","siteuser_id":%s,"account_bank":"","account_name":"","account_number":"","alipay_account":"","pshop_formdata":{},"pshop_level_uuid":"dacefa7f-21af-44ed-9818-2a1f35bb7d45","pshop_level_uuid__toone":{"id":390916994,"uuid":"dacefa7f-21af-44ed-9818-2a1f35bb7d45","data":{"name":"默认等级"},"_resource_uri":"db.datasetrow?dataset_id=391838&table_name=pshop_level&id=390916994"},"siteuser_id__toone":{"id":%s,"namespace":"default","site_id":24860,"group_id":null,"role_id":null,"content_type_id":81,"object_id":24231,"consumer_id":null,"weixin_id":null,"demlution_openid":null,"name":null,"completed":false,"role_verified":false,"is_active":true,"is_temp":false,"is_test":false,"is_deleted":false,"created":"%s","last_modified":"%s","checkin_count":0,"last_checkin":null,"dshareconfig_id":null,"dshareconfig_active_url":null,"dshareconfig_last_modified":null,"source_type":"mobile","source_platform":"mobile","username":"%s","password":null,"nickname":null,"email":null,"email_verified":false,"mobile":"%s","is_wechat":false,"avatar":null,"last_login":null,"last_login_ip":null,"signature":null,"referrer_id":null,"userrank":"","pshop_open":true,"pshop_created":"%s","pshop_state":"open","pshop_parent_id":1953726,"pshop_parent_created":"%s","pshop_money":0,"pshop_withdraw_money":0,"pshop_total_money":0,"pshop_pformdata_id":null,"pshop_level_id":null,"cardid":null,"card_money":"0.00","money_count":"0.00","card_status":"normal","card_created":null,"wx_cardid":null,"card_pformdata_id":null,"branch_id":null,"user_id":null,"card_level_id":null,"card_saler_id":null,"role_pformdata_id":null,"extra":{},"data":{},"_display_avatar":"static/company/m_ucenter/imgs/usercenter_head.jpg","_display_pshop_state":"正常运行","_display_nickname":"%s","_hide_mobile_nickname":"%s","_hide_mobile":"%s","_display_source_platform":"手机","_display_source_type":"手机号注册","_credits_shop":"0","_resource_uri":"db.siteuser?id=%s"},"benefit":0}}}' % (ob_id, sm_name, phone, sm_card, siteuser_id, siteuser_id, created, last_modified, username, mobile, pshop_created, pshop_parent_created, mobile, _hide_mobile_nickname, _hide_mobile_nickname, siteuser_id)
                    return sm_json
            except Exception as e:
                print(e)



    def user_sm(self, phone):
        sm_json = self.re_user_sm(phone)

        sm_url = 'https://m.kaione-sh.cn/dapi/ccode/run?papp_slug=kaiyi&action=member_web.update_auth&pagetemplate_id=107914&dataset_id=391838'
        for nn in range(3):
            try:
                m_time = current_milli_time()
                data = self.dcoding(sm_json, m_time)
                headers = {
                    'Host': 'm.kaione-sh.cn',
                    'Connection': 'keep-alive',
                    'X-Request-Timestamp': '{0}'.format(m_time),
                    'X-Log-Cnickname': 'kywh',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'X-Log-Pid': '987827',
                    'X-Log-Lhash': '#/app_kaiyi-productdetail?product_uuid=9d2d4ee7-915a-49d6-88dc-1acaf9fc5141',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://m.kaione-sh.cn',
                    'Referer': 'https://m.kaione-sh.cn/'
                }
                res = self.session.post(sm_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['result']['status'] == 'error' and (m_json['result']['message'] == '实名认证失败，请检查姓名身份证！' or m_json['result']['message'] == '实名信息已存在！'):
                        sm_json = self.re_user_sm(phone)
                        continue
                    elif m_json['result']['status'] == 'success':
                        logger.info("实名成功")
                        break
                    elif m_json['result']['message_type'] == 'matching_query_does_not_exist':
                        time.sleep(10)
                        sm_json = self.re_user_sm(phone)
                        continue
                    else:
                        time.sleep(10)
                        sm_json = self.re_user_sm(phone)
                        continue
            except Exception as e:
                print(e)

    def user_con_inv(self, phone):
        con_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"member_web.system_preserve","kwargs":{}}'

        con_url = 'https://m.kaione-sh.cn/dapi/ccode/run?papp_slug=kaiyi&action=member_web.system_preserve&pagetemplate_id=107914&dataset_id=391838'
        for nn in range(2):
            try:
                m_time = current_milli_time()
                data = self.dcoding(con_json, m_time)
                headers = {
                    'Host': 'm.kaione-sh.cn',
                    'Connection': 'keep-alive',
                    'X-Log-Cnickname': 'kywh',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Accept': 'application/json, text/plain, */*',
                    'X-Log-Lhash': '#/app_kaiyi-pshopsharetarget',
                    'X-Log-Pid': '987827',
                    'Origin': 'https://m.kaione-sh.cn',
                    'Referer': 'https://m.kaione-sh.cn/?pshop_id={0}'.format(self.uid),
                }
                res = self.session.post(con_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    break
            except Exception as e:
                print(e)


    def set_mark_password(self):
        mp_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"member_web.set_paypassword","kwargs":{"formData":{"password":"","password1":902399,"password2":902399}}}'
        mp_url = 'https://m.kaione-sh.cn/dapi/ccode/run?papp_slug=kaiyi&action=member_web.set_paypassword&pagetemplate_id=107914&dataset_id=391838'

        headers = {
                    'Host': 'm.kaione-sh.cn',
                    'Connection': 'keep-alive',
                    'X-Log-Cnickname': 'kywh',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Accept': 'application/json, text/plain, */*',
                    'X-Log-Lhash': '#/app_kaiyi-pshopsharetarget',
                    'X-Log-Pid': '987827',
                    'Origin': 'https://m.kaione-sh.cn',
                    'Referer': 'https://m.kaione-sh.cn/'
                }
        for nn in range(2):
            try:
                m_time = current_milli_time()
                data = self.dcoding(mp_json, m_time)
                headers = {
                    'Host': 'm.kaione-sh.cn',
                    'Connection': 'keep-alive',
                    'X-Log-Cnickname': 'kywh',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Accept': 'application/json, text/plain, */*',
                    'X-Log-Lhash': '#/app_kaiyi-member_verfiy',
                    'X-Log-Pid': '987827',
                    'Origin': 'https://m.kaione-sh.cn',
                    'Referer': 'https://m.kaione-sh.cn/',
                }
                res = self.session.post(mp_url, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['result']['status'] == 'success':
                        logger.info("设置二级密码成功")
                        break
                    else:
                        print("设置二级密码出错")
                        time.sleep(3)
            except Exception as e:
                print(e)


    def logout(self):
        headers = {
            'Host': 'm.kaione-sh.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'X-Log-Cnickname': 'kywh',
            'X-Log-Pid': '987827',
            'X-Log-Lhash': '#/app_kaiyi-pshopsharetarget',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://m.kaione-sh.cn',
            'Referer': 'https://m.kaione-sh.cn/',
        }
        outurl = 'https://m.kaione-sh.cn/capi/v1/company_account/logout'
        out_json = {}

        for l in range(3):
            try:
                res = self.session.post(outurl, headers=headers, json=out_json, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    break
            except Exception as e:
                logger.info(e)

Ky = KaiYi()