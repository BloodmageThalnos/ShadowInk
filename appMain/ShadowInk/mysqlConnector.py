# -*- coding:utf-8 -*-

import logging
import hashlib
import time
from django.contrib.auth import authenticate
from django.contrib.auth.models import *
from ExploreAPP.models import Article
# from MyCenterAPP.models import PersonalDetails

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

CREATE TABLE `article` (
  `a_id` int(11) NOT NULL AUTO_INCREMENT,
  `u_id` int(11) NOT NULL,
  `title` longtext COLLATE utf8_unicode_ci NOT NULL,
  `pic_url` longtext COLLATE utf8_unicode_ci,
  `content` longtext COLLATE utf8_unicode_ci,
  `create_date` datetime DEFAULT NULL,
  PRIMARY KEY (`a_id`),
  KEY `user_id_idx` (`u_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`u_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



"""

'''

host = "127.0.0.1"
mysql_username = "root"
# 这里改成数据库的密码
mysql_password = "root"
database = "shadowInk"

def md5Password(password):
    h1 = hashlib.md5()
    h1.update(password.encode(encoding="utf-8"))
    h1.update((h1.hexdigest()+"shadowInk").encode(encoding="utf-8"))
    return h1.hexdigest()
    
'''
logger = logging.getLogger(__name__)

# Check the username and password.
# return a set which contains {success, user(if success), message}.
def checkPassword(name, password):
    logger.info('Checking password, name:%s, password:%s' % (name, password))
    if name == None:
        return {'success': False, 'user': None, 'message': '用户名不能为空！'}
    if password == None:
        return {'success': False, 'user': None, 'message': '密码不能为空！'}

    user = authenticate(username=name,password=password)
    if user==None:
        return {'success': False, 'user': None, 'message': '用户名或密码错误！'}
    else:
        return {'success': True, 'user': user, 'message': '欢迎回来，%s，好久不见了！' % (name)}

'''
    if name == None:
        return {'success': False, 'id': 0, 'message': '用户名不能为空！'}
    if password == None:
        return {'success': False, 'id': 0, 'message': '密码不能为空！'}
    logger.info('Checking password, name:%s, password:%s' % (name, password))
    db = mysql.connector.connect        (user=mysql_username, password=mysql_password, database=database)
    cursor = db.cursor()
    cursor.execute("select password,id from User where username = %s",[name])
    result = cursor.fetchall()
    db.close()
    password_md5 = md5Password(password)
    if result is not None and result != []:
        logger.info( str(result) )
        if result[0][0] == password_md5:
            return {'success': True, 'id': result[0][1], 'message': '欢迎回来，%s，好久不见了！' % (name)}
    return {'success': False, 'id': 0, 'message': '用户名或密码错误！'}
'''

# Insert a new record, containing username and password.
def insertUser(name,password):
    logger.info('Inserting new user, name:%s, password:%s' % (name, password))
    user = User.objects.create_user(username=name,password=password,email=None)
    #userDetail = PersonalDetails(user=user,id=user.id)
    #userDetail.save()
    if user==None or user==False:
        return {'success':'False','message':'用户%s已存在！请登录，或重新输入用户名。'%(name)}
    user.save()
    return {'success':'True','message':'注册成功！请登录。'}

'''
def insertUser(name, password):
    logger.info('Setting password, name:%s, password:%s' % (name, password))
    db = mysql.connector.connect(user=mysql_username, password=mysql_password, database=database)
    cursor = db.cursor()
    cursor.execute("select count(*) from user where username = %s",[name])
    result = cursor.fetchall()
    if result[0][0] > 0:
        logger.info('用户名%s已存在,请重新输入' % (name))
        return False
    cursor.execute("insert into User(username,password) values(%s,%s)",[name,md5Password(password)])
    db.commit()
    cursor.close();
    db.close()
    return True
'''


# Get all the users from the database.
# Returns an array of set which contains {id, username, password}.
def getUsers():
    logger.info('Getting all users')
    return User.objects.all()
'''
    logger.info('Getting information')
    db = mysql.connector.connect(user=mysql_username, password=mysql_password, database=database)
    cursor = db.cursor()
    cursor.execute("select id,username,password from User")
    results = cursor.fetchall()
    db.close()
    if results is not None:
        list = []
        for result in results:
            logger.info( str(result) )
            list.append({"id":result[0], "name":result[1],"password":result[2]})
        return list
    return []
'''

# Get the first 10 articles that will be shown on the main page.
# Returns an array of set which contains {title, picurl, content}.
def getArticles():
    logger.info('Getting articles')
    return Article.objects.all()
'''
    logger.info('Getting article')
    db = mysql.connector.connect(user=mysql_username, password=mysql_password, database=database)
    cursor = db.cursor()
    cursor.execute("SELECT title,pic_url,create_date FROM article;")
    results = cursor.fetchall()
    db.close()
    if results is not None:
        list = []
        for result in results:
            list.append({"title":result[0], "picurl":result[1],"time":result[2]})
        return list
    return []
'''

# Insert a new record, containing title, picurl and content.
# return True if no error occurs.
def insertArticle(user, title, picurl, content):
    assert(user!=None)
    logger.info('Inserting article user:%s,title:%s'%(user.username,title))
    article = Article(author=user,title=title,pic_url=picurl,content=content)
    article.save()
'''
    logger.info('Inserting article')
    db = mysql.connector.connect(user=mysql_username, password=mysql_password, database=database)
    cursor = db.cursor()
    cursor.execute("INSERT INTO `article`(`u_id`,`title`,`pic_url`,`content`,`create_date`)\
VALUES(%s,%s,%s,%s,%s);",[str(user_id),title,picurl,content,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())])
    db.commit()
    cursor.close()
    db.close()
    return True
'''
