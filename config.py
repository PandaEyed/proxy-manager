import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://frps:WapShuAsHUa328@rm-bp1332h32z2q71bgu0o.mysql.rds.aliyuncs.com/frps_supplier_manager'
    SQLALCHEMY_TRACK_MODIFICATIONS = False