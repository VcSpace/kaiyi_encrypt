import json
import requests
import time
import os

from logger import logger
from config import global_config

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
}

class JieMa():
    def __init__(self):
        self.m_token = None
        self.pro_id = None  # 项目id
        self.op_id = 0  # (0=默认 4=实卡 5=虚卡) 可为空,请传数字
        self.sm = dict()
        self.create_sm_dict()


        n = global_config.getRaw('jm', 'virtual_card')
        if n == '1':
            self.virtual = True
        elif n == '2':
            self.virtual = False
        else:
            self.virtual = False

        print("是否使用虚拟: ", self.virtual)
        if self.pro_id == None:
            self.pro_id = global_config.getRaw('jm', 'pro_id') #lx 33690 my 56825
            print("项目id: ", self.pro_id)


    def lx_init(self):
        self.lx_user = global_config.getRaw('jm', 'lx_api')
        self.lx_password = global_config.getRaw('jm', 'lx_pd')


    def my_init(self):
        self.my_user = global_config.getRaw('jm', 'my_api')
        self.my_password = global_config.getRaw('jm', 'my_pd')


    def miyun_login(self):
        login_url = 'https://api.miyun999.live/api/login?apiName={0}&password={1}'.format(self.my_user, self.my_password)
        try:
            res = requests.get(login_url, headers=headers, timeout=60)
            logger.info(res.text)
            if res.status_code == 200:
                m_json = json.loads(res.text)
                if m_json['message'] == 'ok':
                    self.m_token = m_json['token']
                    logger.info("米云登陆成功")
                else:
                    logger.info('my登陆失败')
                    time.sleep(1000)
        except Exception as e:
            logger.info(e)

    def get_my_info(self):
        info_url = 'https://api.miyun999.live/api/get_myinfo?token={0}'.format(self.m_token)
        try:
            res = requests.get(info_url, headers=headers, timeout=60)
            logger.info(res.text)
            if res.status_code == 200:
                m_json = json.loads(res.text)
                if m_json['message'] == 'ok':
                    m_money = m_json['money']
                    logger.info("用户余额: %s ", m_money)
        except Exception as e:
            logger.info(e)

    def get_my_phone(self):
        self.phone_num = None
        if self.virtual == True:
            phone_url = 'https://api.miyun999.live/api/get_mobile?token={0}&project_id={1}&api_id=78656764'.format(self.m_token, self.pro_id)
        else:
            phone_url = 'https://api.miyun999.live/api/get_mobile?token={0}&project_id={1}&operator=4&api_id=78656764'.format(self.m_token, self.pro_id)
        while True:
            time.sleep(2)
            try:
                res = requests.get(phone_url, headers=headers, timeout=60)
                logger.info(res.text)
                if res.status_code == 200:
                    m_json = json.loads(res.text)
                    if m_json['message'] == 'ok':
                        phone_num = m_json['mobile']
                        logger.info('获取到手机号 %s', phone_num)
                        return phone_num
                    elif m_json['message'] == '没有可用号码，请休息5秒后再试' or m_json['message']:
                        print('无号码，等待5s')
                        time.sleep(5)
                        continue
                    else:
                        time.sleep(60)
            except Exception as e:
                logger.info(e)

    def get_my_message(self, phone_num):
        message_url = 'https://api.miyun999.live/api/get_message?token={0}&project_id={1}&phone_num={2}'.format(self.m_token, self.pro_id, phone_num)
        for l in range(20):
            try:
                res = requests.get(message_url, headers=headers, timeout=30)
                if res.status_code == 200:
                    m_json = json.loads(res.text)
                    print(res.text)
                    if m_json['message'] == 'ok':
                        logger.info(res.text)
                        mes_code = m_json['code']
                        return mes_code
                    elif m_json['message'] == 'token已失效':
                        logger.info(res.text)
                        time.sleep(1000)
                    else:
                        print('未取到短信，请等待3s')
                        time.sleep(3)
            except Exception as e:
                logger.info(e)

        self.detail_my_phone(phone_num)

    def detail_my_phone(self, phone_num):
        de_phone = 'https://api.miyun999.live/api/add_blacklist?token={0}&project_id={1}&phone_num={2}'.format(self.m_token, self.pro_id, phone_num)
        try:
            res = requests.get(de_phone, headers=headers, timeout=30)
            if res.status_code == 200:
                m_json = json.loads(res.text)
                if m_json['message'] == 'ok':
                    logger.info('拉黑手机号: %s',phone_num)
        except Exception as e:
            logger.info(e)


    ###-----------------------------
    def lx_login(self):
        login_url = 'http://api.lx967.com:9090/sms/api/login?username={0}&password={1}'.format(self.lx_user, self.lx_password)
        try:
            res = requests.get(login_url, headers=headers, timeout=60)
            logger.info(res.text)
            if res.status_code == 200:
                m_json = json.loads(res.text)
                if m_json['code'] == 0:
                    self.m_token = m_json['token']
                    logger.info("lx登陆成功")
                else:
                    logger.info('lx登陆失败')
                    time.sleep(1000)
        except Exception as e:
            logger.info(e)
    def get_lx_info(self):
        info_url = 'http://api.lx967.com:9090/sms/api/userinfo?token={0}'.format(self.m_token)
        try:
            res = requests.get(info_url, headers=headers, timeout=60)
            logger.info(res.text)
            if res.status_code == 200:
                m_json = json.loads(res.text)
                if m_json['code'] == 0:
                    m_money = m_json['money']
                    logger.info("用户余额: %s ", m_money)
        except Exception as e:
            logger.info(e)

    def get_lx_phone(self):
        phone_url = ''
        if self.virtual == False:
            phone_url = 'http://api.lx967.com:9090/sms/api/getPhone?token={0}&sid={1}&ascription=1'.format(self.m_token, self.pro_id)
        else:
            phone_url = 'http://api.lx967.com:9090/sms/api/getPhone?token={0}&sid={1}'.format(self.m_token, self.pro_id)


        while True:
            try:
                res = requests.get(phone_url, headers=headers, timeout=60)
                logger.info(res.text)
                if res.status_code == 200:
                    m_json = json.loads(res.text)
                    if m_json['code'] == 0:
                        phone = m_json['phone']
                        logger.info('获取到手机号 %s', phone)
                        return phone
                    elif m_json['code'] == -1:
                        print('无号码，等待5s')
                        time.sleep(5)
                        continue
                    else:
                        time.sleep(5000)
            except Exception as e:
                logger.info(e)

    def get_lx_message(self, phone):
        message_url = 'http://api.lx967.com:9090/sms/api/getMessage?token={0}&sid={1}&phone={2}&tid=105188'.format(self.m_token, self.pro_id, phone)
        for l in range(20):
            try:
                res = requests.get(message_url, headers=headers, timeout=30)
                if res.status_code == 200:
                    m_json = json.loads(res.text)
                    m_code = m_json['code']
                    if m_code == 0:
                        logger.info(res.text)
                        mes_code = m_json['code']
                        mes_code = "".join(list(filter(str.isdigit, m_json['sms'])))
                        return mes_code
                    elif m_code == -4 or m_code == -1:
                        print('未取到短信，请等待3s')
                        time.sleep(3)
                    else:
                        logger.info(res.text)
                        time.sleep(5)
            except Exception as e:
                logger.info(e)

        self.detail_lx_phone(phone)

    def detail_lx_phone(self, phone):
        de_phone = 'http://api.lx967.com:9090/sms/api/cancelRecv?token={1}&sid={1}&phone={2}'.format(self.m_token, self.pro_id, phone)
        try:
            res = requests.get(de_phone, headers=headers, timeout=30)
            if res.status_code == 200:
                m_json = json.loads(res.text)
                if m_json['code'] == 0:
                    logger.info('拉黑手机号: %s', phone)
        except Exception as e:
            logger.info(e)



    def init_jm(self, choose):
        if choose == '1':
            self.my_init()
            self.miyun_login()
            self.get_my_info()
        elif choose == '2':
            self.lx_init()
            self.lx_login()
            self.get_lx_info()
    #         self.get_lx_phone()
    #         # self.get_lx_message(phone)

    def get_phone(self, cho):
        if cho == '1':
            return self.get_my_phone()
        elif cho == '2':
            return self.get_lx_phone()

    def get_message(self, cho, phone):
        if cho == '1':
            return self.get_my_message(phone)
        elif cho == '2':
            return self.get_lx_message(phone)

    def detail_phone(self, cho, phone):
        if cho == '1':
            self.detail_my_phone(phone)
        elif cho == '2':
            self.detail_lx_phone(phone)

    def get_ip(self):
        ipurl = 'http://api1.ydaili.cn/tools/BMeasureApi.ashx?action=BEAPI&secret=B29A8906A8B75EFD7485C8B5A77E30DEA2A1FD0DB3F5E262&number=1&orderId=34550&format=json'
        req = requests.get(ipurl)
        tjson = json.loads(req.text)
        if tjson['status'] == 'success':
            get_ip = tjson['data'][0]
            ip = get_ip['IP']
            return ip

    def create_sm_dict(self):
        lines = 0
        with open("./zin.mtcsdfv", "r") as f:
            for line in f.readlines():
                m_line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                if m_line == '':
                    continue
                lines = lines + 1
                sep = '----'
                name = line.split(sep, 1)[0]
                if name != '':
                    card = m_line.split(sep)[1]
                self.sm[name] = card
        print('\n读取lz %s行' % lines)


    def get_sm(self):
        pop_obj = self.sm.popitem()
        self.del_line('./zin.mtcsdfv')
        return pop_obj[0], pop_obj[1]


    def del_line(self, filename):
        file_old = open(filename, 'rb+')
        m = 24
        # 1.定位文件末尾的前m个字符的位置，大小可根据每一行的字符数量修改，为一估计值，但不能超过文件总字符数
        # 若要删除最后一行，要确保m比最后一行的字符数大
        # 若要删除后N行，要确保后N行的总字符数比m小
        # 若文件很小或无法大体估计每一行的字符数，可以删除这行代码
        # 2.从步骤1定位的位置开始读取接下来的每一行数据，若步骤1的代码删除，则会从文件头部开始读取所有行
        lines = file_old.readlines()

        # 3.定位到最后一行的行首，若要删除后N行，将lines[-1]改为lines[-N:]即可
        file_old.seek(-len(lines[-1]), os.SEEK_END)
        file_old.truncate()  # 截断之后的数据
        file_old.close()


JM = JieMa()