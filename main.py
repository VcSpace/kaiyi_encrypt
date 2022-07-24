import execjs
import time
import os


#https://zhuanlan.zhihu.com/p/59585033

current_milli_time = lambda: int(round(time.time() * 1000))


if __name__ == '__main__':
    js_env = execjs.get()
    m_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"productitem_web.list","kwargs":{"limit":10,"offset":0,"filters":{"data__name__icontains":"农田","data__category_uuid":null},"order_by":["data__saleprice__int"]}}'
    m_time = current_milli_time()
    res = None
    with open('./c9ed10dc.js') as f:
        ctx = execjs.compile(f.read())
        res = ctx.call("jsstart", m_json, m_time)
    print(res)