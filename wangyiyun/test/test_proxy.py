# coding: utf-8

import requests

# noinspection PyPep8Naming
def validUsefulProxy(proxy):
    """
    检验代理是否可用
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf8')
    proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    try:
        # 超过20秒的代理就不要了
        r = requests.get('http://www.baidu.com', proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200 and r.json().get("origin"):
            # logger.info('%s is ok' % proxy)
            return True
    except Exception as e:
        # logger.error(str(e))
        return False

proxy = "120.234.63.196:8892"

# print(validUsefulProxy(proxy))

proxies = {"http": "http://{p}".format(p=proxy), "https": "http://{p}".format(p=proxy)}
db_url = "http://www.baidu.com"
rep = requests.get(db_url, proxies=proxies)
print(rep.text)
