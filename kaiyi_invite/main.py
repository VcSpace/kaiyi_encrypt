import execjs
import time
import os
import threading

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
    t1 = threading.Thread(target=Ky.invite, args=())
    t2 = threading.Thread(target=Ky.invite, args=())

    t1.start()
    # t2.start()

    t1.join()
    # t2.join()

    # Ky.invite()
    # Ky.login()

