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



if __name__ == '__main__':
    #农田抄底
    Ky.login()
    m_pro = input('输入检测商品')
    while True:
        Ky.seckill_low(m_pro)


