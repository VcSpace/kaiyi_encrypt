import json
import requests
import time
import random

from threading import Thread
from time import sleep, ctime
from logger import logger
# from jm import JM

headers = {
    'Host': 'm.kaione-sh.cn',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://m.kaione-sh.cn',
    'Referer': 'https://m.kaione-sh.cn/?pshop_id=1936026',
    'Cookie': 'da_a=24e59260d1aa44d5a930722862993432'
}

class KaiYi():
    def __init__(self):
        self.session = requests.Session()
        self.session2 = requests.Session()
        self.test_password = 'KKKMMQ1'
        self.user_password = 'Kyzxz456123'

    def gogogo(self):
        with open("./708out_success.txt", "r") as f:
            for line in f.readlines():
                m_line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                if m_line == '':
                    print('结束')
                    time.sleep(2222)
                sep = '----'
                phone = m_line.split(sep, 1)[0]
                self.start(phone)


    def start(self, phone):
        time.sleep(5)
        for ll in range(1):
            ip= self.get_ip()
            print(ip)
            self.proxies = {
                "http": "http://{0}".format(ip),
                "https": "http://{0}".format(ip),
            }

            # phone = JM.get_phone(cho)
            # flag = False
            # requests.get('https://m.kaione-sh.cn/?pshop_id=1936026#/app_kaiyi-pshopsharetarget', headers=headers, timeout=20)
            # flag = self.ex_olduser(phone)
            # if flag == True:
            #     get_flag = self.sendmessage(phone)
            #     if get_flag == False:
            #         JM.detail_phone(cho, phone)
            #         continue
            #     m_code = JM.get_message(cho, phone)
            #     if m_code == None:
            #         continue
            self.ky_login(phone)



    def get_ip(self):
        ipurl = 'http://api1.ydaili.cn/tools/BMeasureApi.ashx?action=BEAPI&secret=B29A8906A8B75EFD7485C8B5A77E30DEA2A1FD0DB3F5E262&number=1&orderId=34550&format=json'
        req = requests.get(ipurl)
        tjson = json.loads(req.text)
        if tjson['status'] == 'success':
            get_ip = tjson['data'][0]
            ip = get_ip['IP']
            return ip

    def ex_olduser(self, phone):
        m_json = {"username":"{0}".format(phone),
                  "password": "{0}".format(self.test_password)
        }
        url = 'https://m.kaione-sh.cn/capi/v1/company_account/login'
        try:
            res = requests.post(url, headers=headers, json=m_json, proxies=self.proxies, timeout=60)
            if res.status_code == 200:
                m_json = json.loads(res.text)
                logger.info("%s ----%s", res.text, phone)
                if m_json['message'] == '用户不存在' or m_json['message_type'] == 'siteuser_404':
                    return True
                else:
                    return False
        except Exception as e:
            logger.info(e)

    def sendmessage(self, phone):
        send_url = 'https://m.kaione-sh.cn/dapi/verification_code/send_verify_code'
        send_json = {
            "mobile":"{0}".format(str(phone))
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
                        print("短信发送失败正在重试----%d次", send)
                        time.sleep(3)
            except Exception as e:
                logger.info(e)
        return False

    def reg_user(self, phone, m_code):
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
            'Referer': 'https://m.kaione-sh.cn/?pshop_id=1936026',
            'Cookie': 'da_a=24e59260d1aa44d5a930722862993432; __snaker__id=bzEgpceaRyr2oxl8; gdxidpyhxdE=Km8%5Cs2DCkHJCLgqDifpESjbGHMgRb88lpTLlf22BhRXlrj6msYozH99mCVJPYX%5CWkxCAGB21DEHNrEUguKzqjUxvc%5CGcLKgmThwzvt3hmiCGAY1xu9heQzKy5bOY%2BI5LBqgIRM75lwPQqd6z0%2FvbCmNkP1PCHaJLXtVno%2B111V21Uesz%3A1654235917520; _9755xjdesxxd_=32; YD00054829761180%3AWM_NI=RaK6wbzOkkPAzwhch0F9g505lRWRcbBlMsZM75CMp9KnlFnrQ0w3jjmEHnQh7wYGLai3LwJJj%2BhUZANoKS12XZDtPrtbmwp3JwsJjAADa5ObxEcf5DyvMDg9X5ZQwvFeTmg%3D; YD00054829761180%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eea6b23bfbae978dcc59f4b88eb6c55a939e9facd85ea9b29eb7fc33a296b8d1e72af0fea7c3b92a92bf85d7f66aba91a58cd34bbaa9a884eb3c86e7a9d6b33fb08e99b3e26a82b48394d947f5eb8daef33389b2a4a7ed7a93f0b9d4e962af9b888fd464f5a997a8cf6babed8498c942aaf5a8b6d94b8eb185b4b43a9c868c95d37ab8bea398f3398aa9bdabe94b839cafd6ce6abc9bad87b850bbaa83a5e6339ceb96b2f67e86bb9c8ee637e2a3; YD00054829761180%3AWM_TID=mkk5WoOdwyRBQUBFEFfRAx3AR3ofd0lI'
        }
        reg_url = 'https://m.kaione-sh.cn/capi/v1/company_account/signup_with_mobile'
        reg_json = {
            "mobile":"{0}".format(phone),
            "code":"{0}".format(m_code),
            "password1":"{0}".format(self.user_password),
            "password2":"{0}".format(self.user_password),
            "invitation_code":""
        }
        for l in range(3):
            try:
                res = self.session.post(reg_url, headers=headers, json=reg_json, proxies=self.proxies,timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['status'] == 'success' or m_json['message'] == '登陆成功':
                        logger.info("注册成功----%s----%s", phone, self.user_password)
                        with open("./reg_success.txt", "a") as file:
                            file.write(phone + '----' + self.user_password + '\n')
                            self.ky_login(phone)
                        break
                with open("account/reg_error.txt", "a") as file:
                    file.write(phone + '----' + self.user_password + '\n')
            except Exception as e:
                logger.info(e)

    def ky_login(self, phone):
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
        login_url = 'https://m.kaione-sh.cn/capi/v1/company_account/login'
        login_json = {
            "username": "{0}".format(phone),
            "password": "{0}".format(self.user_password)
        }

        for l in range(3):
            try:
                res = self.session2.post(login_url, headers=headers, json=login_json, proxies=self.proxies,timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['message_type'] == 'login_success' or m_json['message'] == '登陆成功':
                        logger.info("登录成功----%s----%s", phone, self.user_password)
                        self.set_userinfo()
                        self.logout(phone)
                        break
                with open("./login_error.txt", "a") as file:
                    file.write(phone + '----' + self.user_password + '\n')
            except Exception as e:
                logger.info(e)

    def set_userinfo(self):
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
            "nickname":"{0}".format(random_str)
        }

        for l in range(3):
            try:
                res = self.session2.post(user_url, headers=headers, json=user_json, proxies=self.proxies, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['status'] == 'success' or m_json['message'] == '用户信息设置成功':
                        logger.info("用户资料设置成功")
                        break
            except Exception as e:
                logger.info(e)



    def logout(self, phone):
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
                res = self.session2.post(outurl, headers=headers, json=out_json, proxies=self.proxies, timeout=60)
                if res.status_code == 200:
                    logger.info(res.text)
                    m_json = json.loads(res.text)
                    if m_json['status'] == 'success' or m_json['message'] == 'logout_success':
                        logger.info("退出成功----%s----%s", phone, self.user_password)
                        with open("./out_success.txt", "a") as file:
                            file.write(phone + '----' + self.user_password + '\n')
                        break
                with open("./out_error.txt", "a") as file:
                    file.write(phone + '----' + self.user_password + '\n')
            except Exception as e:
                logger.info(e)

KY = KaiYi()

if __name__ == '__main__':
    KY.gogogo()