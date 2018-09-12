import logging

logger = logging.getLogger(__name__)

# Check the username and password.
# Returns None if password is wrong, otherwise return userId.
def checkPassword(name, password):
    logger.info('Checking password, name:%s, password:%d'%(name,password))
    
    if name==password: 
        return 1
    else:
        return None

        
# Insert a new record, containing username and password.
def insertUser(name, password):
    logger.info('Setting password, name:%s, password:%d'%(name,password))
    
    
    
# Get all the users from the database.
# Returns an array of set which contains {username, password}.
def getUsers():
    logger.info('Getting information')
    
    return [{name:'18810339563',password:'12****78'},{name:'TestAccount',password:'Te********rd'}]
    

