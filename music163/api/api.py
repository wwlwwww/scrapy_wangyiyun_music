# coding: utf-8
import base64
import binascii
import hashlib
import json
import os
# from http.cookiejar import Cookie
from http.cookiejar import Cookie

import requests
from requests import cookies

from music163.spiders.proxy_handler import ProxyHandler

__all__ = ["encrypted_id", "encrypted_request"]

MODULUS = (
    "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7"
    "b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280"
    "104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932"
    "575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b"
    "3ece0462db0a22b8e7"
)
PUBKEY = "010001"
NONCE = b"0CoJUm6Qyw8W8jud"
from Cryptodome.Cipher import AES


# 歌曲加密算法, 基于https://github.com/yanunon/NeteaseCloudMusic
def encrypted_id(id):
    magic = bytearray("3go8&$8*3*3h0k(2)2", "u8")
    song_id = bytearray(id, "u8")
    magic_len = len(magic)
    for i, sid in enumerate(song_id):
        song_id[i] = sid ^ magic[i % magic_len]
    m = hashlib.md5(song_id)
    result = m.digest()
    result = base64.b64encode(result).replace(b"/", b"_").replace(b"+", b"-")
    return result.decode("utf-8")


# 登录加密算法, 基于https://github.com/stkevintan/nw_musicbox
def encrypted_request(text):
    # type: (str) -> dict
    data = json.dumps(text).encode("utf-8")
    secret = create_key(16)
    params = aes(aes(data, NONCE), secret)
    encseckey = rsa(secret, PUBKEY, MODULUS)
    return {"params": params, "encSecKey": encseckey}


def aes(text, key):
    pad = 16 - len(text) % 16
    text = text + bytearray([pad] * pad)
    encryptor = AES.new(key, 2, b"0102030405060708")
    ciphertext = encryptor.encrypt(text)
    return base64.b64encode(ciphertext)


def rsa(text, pubkey, modulus):
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16), int(pubkey, 16), int(modulus, 16))
    return format(rs, "x").zfill(256)


def create_key(size):
    return binascii.hexlify(os.urandom(size))[:16]

BASE_URL = "http://music.163.com"

DEFAULT_TIMEOUT = 5


# 评论
def song_comments(music_id, offset=0, total="false", limit=100):
    path = "/weapi/v1/resource/comments/R_SO_4_{}/".format(music_id)
    params = dict(rid=music_id, offset=offset, total=total, limit=limit)
    # return self.request("POST", path, params)
    return path, params

 # 热门评论
def song_hot_comments(music_id, offset=0, total="false", limit=100):
    # 客户端热门评论，每页101个评论 http://music.163.com/weapi/v1/resource/hotcomments/R_SO_4_
    path = "/weapi/v1/resource/hotcomments/R_SO_4_{}/".format(music_id)
    params = dict(rid=music_id, offset=offset, total=total, limit=limit)
    # return self.request("POST", path, params)
    return path, params

# song ids --> song urls ( details )
def songs_detail(ids):
    path = "/weapi/v3/song/detail"
    params = dict(c=json.dumps([{"id": _id} for _id in ids]), ids=json.dumps(ids))
    # return self.request("POST", path, params).get("songs", [])
    return path, params

HEADERS = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        # "Host": "music.163.com",
        "Referer": "http://music.163.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
}


def raw_request(method, url, params={}):
    headers = HEADERS

    csrf_token = ""
    params.update({"csrf_token": csrf_token})
    params = encrypted_request(params)
    # print("params:", params)

    # cookies = {'os': 'android'}
    cookies = {}

    while True:
        proxy_rsp = ProxyHandler.random_get()
        if proxy_rsp != "":
            tmp_proxy = 'http://' + proxy_rsp
            tmp_proxy = 'http://127.0.0.1:12759'
            proxies = {"http": tmp_proxy,
                       "https": tmp_proxy,
            }
            # proxies = {}
            try:
                if method == "GET":
                    # url = 'http://httpbin.org/cookies'
                    resp = requests.get(
                        url, params=params, headers=headers, timeout=DEFAULT_TIMEOUT, proxies=proxies, cookies=cookies
                    )
                elif method == "POST":
                    # url = 'http://httpbin.org/cookies'
                    resp = requests.post(
                        url, data=params, headers=headers, timeout=DEFAULT_TIMEOUT, proxies=proxies, cookies=cookies
                    )
                return resp
            except Exception as e:
                print(e)
                break

# artist_id --> albums
def get_artist_album(artist_id, offset=0, limit=200):
    path = "/weapi/artist/albums/{}".format(artist_id)
    params = dict(offset=offset, total=True, limit=limit)
    return path, params

# album id --> song id set
def album(album_id):
    path = "/weapi/v1/album/{}".format(album_id)
    return path, dict()

if __name__ == "__main__":
    # print(m.login("1223292709@qq.com", "WML13938182619"))
    relative_path, params = song_comments(411214279)
    # relative_path, params = album(43650)
    relative_path, params = get_artist_album(1012032)
    print(raw_request("POST", BASE_URL + relative_path + "?abc=xyz", params).json())

