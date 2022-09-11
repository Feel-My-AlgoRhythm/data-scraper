import pymysql
import configparser

config = configparser.ConfigParser()
config.read_file(open('config/config.default.ini'))

class Database:
    def __init__(self):
        self.session = pymysql.connect(
            host=config['DATABASE']['HOST'],
            port=int(config['DATABASE']['PORT']),
            user=config['DATABASE']['USER'],
            password=config['DATABASE']['PASSWORD'],
            db=config['DATABASE']['DB'],
            charset=config['DATABASE']['CHARSET'],
        )
        self.cursor = self.session.cursor(pymysql.cursors.DictCursor)
