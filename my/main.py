# -*- coding:utf-8 -*-

import logging

logger = logging.getLogger(__name__)

# Check the username and password.
# return a set which contains {success, id, message}.
def checkPassword(name, password):
    logger.info('Checking password, name:%s, password:%s'%(name,password))
    
    if name==password: 
        return {'success':True, 'id':1, 'message':'欢迎回来，%s，好久不见了！'%(name)}
    else:
        return {'success':False, 'id':0, 'message':'用户名或密码错误！'}

        
# Insert a new record, containing username and password.
def insertUser(name, password):
    logger.info('Setting password, name:%s, password:%s'%(name,password))
    
    
    
# Get all the users from the database.
# Returns an array of set which contains {username, password}.
def getUsers():
    logger.info('Getting information')
    
    return [{'name':'18810339563','password':'12****78'},{'name':'TestAccount','password':'Te********rd'}]
    

