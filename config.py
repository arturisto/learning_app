import os

basedir = os.path.abspath(
     os.path.dirname(__file__)
)

class Config:
    pass

class DevConfig(Config):
    SECRET_KEY = "arandomsecretkey"

    SQLALCHEMY_DATABASE_URI= "sqlite:///" + os.path.join(basedir, "app.db")

    MAIL_SERVER     = "smtp.gmail.com"
    MAIL_PORT       = 587
    MAIL_USE_TLS    = True
    MAIL_USE_SSL    = False
    MAIL_USERNAME   = 'arthurruthenberg@gmail.com '
    MAIL_PASSWORD   = 'b3cFlJ9Y'

class ProdConfig(Config):

    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    # SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_DATABASE_URI ='postgresql://postgres:1@localhost:5432/app_db'
    SECRET_KEY = "1265ewqtfsdaxvgz9287ynx918u2nx8172m301u9"

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'arthurruthenberg@gmail.com '
    MAIL_PASSWORD = 'b3cFlJ9Y'

config = {
    "development": DevConfig,
    "production": ProdConfig
}