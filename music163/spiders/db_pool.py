# -*-coding:utf-8-*-


import DBUtils
import pymysql

# db = pymysql.connect(host="172.27.0.10", port=3306, user="root", password="wmlhust12", db="music163")
pool = DBUtils.PersistentDB(creator=pymysql, maxusage=100, host="172.27.0.10", port=3306, user="root", password="wmlhust12", database="music163", charset='utf8')