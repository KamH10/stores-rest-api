import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# from datetime import timedelta        # HEROKU - commented out

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
app = Flask(__name__)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
app.config['DEBUG'] = True      # HEROKU

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../sqlite3DB/data.db'
#
# This indicates that when in Heroku use the 'DATABASE_URL' variable that 
# points to the Postgres DB link. Also when working locally and the 
# 'DATABASE_URL' doesn’t exist, we continue using 'sqlite:///data.db'.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')         # HEROKU

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=600)    # 10 minutes   # HEROKU - commented out
# app.config['PROPAGATE_EXCEPTIONS'] = True     # HEROKU - commented out

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
app.secret_key = 'tyler'
api = Api(app)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# HEROKU - commented out
# @app.before_first_request
# def create_tables():
#     db.create_all()

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
jwt = JWT(app, authenticate, identity)  # /auth

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:             # HEROKU
        @app.before_first_request
        def create_tables():
            db.create_all()

    # app.run(port=5000)
    app.run()                           # HEROKU
