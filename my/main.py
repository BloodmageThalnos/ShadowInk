# -*- coding:utf-8 -*-

import logging
import mysql.connector
import hashlib

"""
这里数据库的名字是shadowInk
用户表为user
有三列
id 主键,自增
username 非空 unique
password 非空

CREATE DATABASE `shadowink` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;

USE shadowink;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

"""

host = "127.0.0.1"
mysql_username = "root"
# 这里改成数据库的密码
mysql_password = "root"
database = "shadowInk"
logger = logging.getLogger(__name__)

def md5Password(password):
    h1 = hashlib.md5()
    h1.update(password.encode(encoding="utf-8"))
    h1.update((h1.hexdigest()+"shadowInk").encode(encoding="utf-8"))
    return h1.hexdigest()

# Check the username and password.
# return a set which contains {success, id, message}.
def checkPassword(name, password):
    if name == None:
        return {'success': False, 'id': 0, 'message': '用户名不能为空！'}
    if password == None:
        return {'success': False, 'id': 0, 'message': '密码不能为空！'}
    logger.info('Checking password, name:%s, password:%s' % (name, password))
    db = mysql.connector.connect(user=mysql_username, password=mysql_password, database="shadowInk")
    cursor = db.cursor()
    cursor.execute("select password from User where username = %s",[name])
    result = cursor.fetchall()
    db.close()
    password_md5 = md5Password(password)
    if result is not None and result != []:
        logger.info( str(result) )
        if result[0][0] == password_md5:
            return {'success': True, 'id': 1, 'message': '欢迎回来，%s，好久不见了！' % (name)}
    return {'success': False, 'id': 0, 'message': '用户名或密码错误！'}


# Insert a new record, containing username and password.
def insertUser(name, password):
    logger.info('Setting password, name:%s, password:%s' % (name, password))
    db = mysql.connector.connect(user=mysql_username, password=mysql_password, database="shadowInk")
    cursor = db.cursor()
    cursor.execute("select count(*) from User where username = %s",[name])
    result = cursor.fetchall()
    if result[0][0] > 0:
        logger.info('用户名%s已存在,请重新输入' % (name))
        return False
    cursor.execute("insert into User(username,password) values(%s,%s)",[name,md5Password(password)])
    db.commit()
    cursor.close();
    db.close()
    return True

# Get all the users from the database.
# Returns an array of set which contains {username, password}.
def getUsers():
    logger.info('Getting information')
    db = mysql.connector.connect(user=mysql_username, password=mysql_password, database=database)
    cursor = db.cursor()
    cursor.execute("select username from User")
    results = cursor.fetchall()
    db.close()
    if results is not None:
        list = []
        for result in results:
            list.append({"name":result[0],"password":result[1]})
        return list
    return []