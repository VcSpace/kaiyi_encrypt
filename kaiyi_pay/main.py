import execjs
import time
import os

from kai import Ky

os.environ["EXECJS_RUNTIME"] = "Node"


#https://zhuanlan.zhihu.com/p/59585033

current_milli_time = lambda: int(round(time.time() * 1000))

"""
function jsstart(m_json, m_time) {
   t = fT(m_json, m_time)
   return t
}
"""

def del_line(filename):
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

if __name__ == '__main__':

    phone_lines = 0
    phone_list = dict()
    tian_file = './reg_success.txt'
    with open(tian_file, "r") as f:
        for line in f.readlines():
            m_line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            if m_line == '':
                continue
            phone_lines = phone_lines + 1
            sep = '----'
            phone = line.split(sep, 1)[0]
            if phone != '':
                pwd = m_line.split(sep)[1]
                phone_list[phone] = pwd

    print('读取phone %s行' % phone_lines)
    n = 0

    while True:
        pop_obj = phone_list.popitem()
        phone, password = pop_obj[0], pop_obj[1]
        print(password)
        print("当前号码 %s" % phone)

        Ky.store_login(phone, password)

        uuid = Ky.five_pay()
        order_id = Ky.create_order(uuid)
        # print(uuid, order_id)
        pay_url = Ky.pay_order(uuid, order_id)
        print(pay_url)
        Ky.login(phone, password, uuid, pay_url)

        del_line(tian_file)