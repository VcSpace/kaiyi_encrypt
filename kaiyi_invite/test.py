# m_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"productitem_web.list","kwargs":{"limit":10,"offset":0,"filters":{"data__name__icontains":null,"data__category_uuid":"%s"},"order_by":["data__saleprice__int"]}}' % '农田'
# print(m_json)
#
# m_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"productitem_order.submit","kwargs":{"productitem_uuid":"%s"}}' % 'qqqqq-wdddqwd-qq'
# print(m_json)

import execjs
import time
import os
import json
import requests
import keyboard

os.environ["EXECJS_RUNTIME"] = "Node"
current_milli_time = lambda: int(round(time.time() * 1000))


def dcoding(m_json, m_time):
    # js_env = execjs.get().name
    res = None
    with open('./c9ed10dc.js') as f:
        ctx = execjs.compile(f.read())
        res = ctx.call("jsstart", m_json, m_time)
    return res

if __name__ == '__main__':
    m_json = '{"is_admin":false,"pagetemplate_id":107914,"dataset_id":391838,"action":"order_web.detail","kwargs":{"uuid":"0ff88b6c-3243-493a-98ff-3001bc6056c0"}}'
    m_time = 1658746717640
    print(dcoding(m_json, m_time))