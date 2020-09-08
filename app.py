from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister,User,UserLogin
from resources.product import Product,Products

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'apu'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)
# Fetch product using product name
api.add_resource(Product,'/product/<string:product_name>')
# fetch all products
api.add_resource(Products,'/products')

# USER registration | pass->username and password
api.add_resource(UserRegister,'/register')
# Fetch username and id
api.add_resource(User,'/user/<string:username>')
# USER Login | pass->username and password
api.add_resource(UserLogin,'/login')



if __name__=='__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000,debug=True)
