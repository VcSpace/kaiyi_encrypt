import execjs
import time
import os

os.environ["EXECJS_RUNTIME"] = "Node"


#https://zhuanlan.zhihu.com/p/59585033

current_milli_time = lambda: int(round(time.time() * 1000))

"""
function jsstart(m_json, m_time) {
   t = fT(m_json, m_time)
   return t
}
"""


    js_env = execjs.get().name
    print(js_env)
    m_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"productitem_web.list","kwargs":{"limit":10,"offset":0,"filters":{"data__name__icontains":"管中窥豹-Ⅰ","data__category_uuid":"3a14d5cc-dab7-4338-b2ea-3b56cacccfe4"},"order_by":["data__saleprice__int"]}}'
    m_time = current_milli_time()
    print(m_time)
    res = None
    with open('./c9ed10dc.js') as f:
        ctx = execjs.compile(f.read())
        res = ctx.call("jsstart", m_json, m_time)
    print(res)

if __name__ == '__main__':