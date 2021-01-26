import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
    S3_KEY = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    BT_MERCHANT_ID= os.environ.get("BT_MERCHANT_ID")
    BT_PUBLIC_KEY= os.environ.get("BT_PUBLIC_KEY")
    BT_PRIVATE_KEY= os.environ.get("BT_PRIVATE_KEY")
    #MAILGUN_API_KEY = os.environ.get("MG_PRIVATE_KEY")
   # MAILGUN_DOMAIN = os.environ.get("MG_DOMAIN")
   # MAILGUN_RECIPIENT = os.environ.get("MG_RECIPIENT")
    G_CLIENT_ID = os.environ.get("OAUTH_ID")
    G_CLIENT_SECRET = os.environ.get("OAUTH_SECRET")


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
