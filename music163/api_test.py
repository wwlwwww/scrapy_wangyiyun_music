# coding: utf-8
import requests
from music163.spiders.Proxy_handler import ProxyHandler


def get_song_comments(music_id, offset=0, total='false', limit=100):
    action = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}/?rid=R_SO_4_{}&\
            offset={}&total={}&limit={}'.format(music_id, music_id, offset, total, limit)

    # proxy = {"http": "http://dev-proxy.oa.com:8080"}
    # proxy = {"http": "http://194.182.74.160:3128"}
    # proxy = {"http": "http://127.0.0.1:1080"}

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
               "Referer": "Referer:http://music.163.com/",
               "Accept-Encoding": "zh-CN,zh;q=0.8,en;q=0.6",
               "Content-Type": "application/x-www-form-urlencoded",
               }

    # rep = requests.get(action, proxies=proxy, headers=headers)
    rep = requests.get(action, headers=headers)
    print("status code:", rep.status_code)
    return rep


def get_hot_comments(rep):
    comments_list = []
    comments = rep.json()['hotComments']
    for comment in comments:
        tmp_dict = {}
        tmp_dict['nickname'] = comment['user']['nickname']
        tmp_dict['star_cnt'] = comment['likedCount']
        tmp_dict['content'] = comment['content']
        if len(comment['beReplied']) > 0:
            tmp_dict['quote'] = comment['beReplied'][0]['content']
        # log.msg(tmp_dict, _level=log.INFO)
        comments_list.append(tmp_dict)

    return comments_list


if __name__ == "__main__":
    rep = get_song_comments(520521342)
    print(rep.text)
    # print(get_hot_comments(rep))
    # tmp_proxy = ProxyHandler.random_get()
    # proxy = {"http": tmp_proxy}
    # rep = requests.get("http://httpbin.org/ip", timeout=(2, 8))
    # print(rep.text)
