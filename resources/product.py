from datetime import datetime
import werkzeug
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.product import ProductModel


class Product(Resource):
    # parsing data received from user
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('product_category',
                        type=str,
                        required=True,
                        help="Every item needs product_category."
                        )
    parser.add_argument('quantity',
                        type=int,
                        required=True,
                        help="Quantity cannot be left blank!"
                        )
    parser.add_argument('exp_date',
                        type=str,
                        required=True,
                        help="exp_date cannot be left blank!"
                        )
    parser.add_argument('manufacturing_date',
                        type=str,
                        required=True,
                        help="manufacturing_date cannot be left blank!"
                        )

    # get product details by passing product_name
    def get(self,product_name):
        item = ProductModel.find_by_name(product_name)
        if item:
            item_json = item.json()
            item_json['is_expired'] = ProductModel.convert_to_cst_time(datetime.now()) > item.exp_date
            return item_json,200

        return {'message':'Product not found'},404

    # store product_details to database
    def post(self,product_name):
        if ProductModel.find_by_name(product_name):
            return {'message':f'An item with name {product_name} already exists'},400

        data = Product.parser.parse_args()

        # converting exp_date and manufacturing_date to CST time

        exp_date = ProductModel.convert_to_cst_time(data['exp_date'])
        manufacturing_date = ProductModel.convert_to_cst_time(data['manufacturing_date'])
        item = ProductModel(product_name,data['product_category'],data['price'],data['quantity'],exp_date,
                            manufacturing_date)
        try:
            item.save_to_db()
        except:
            return {"message":"An error occurred inserting the item."},500

        return {"message":f'ADDED TO DB {item.json()}'},201

    # soft DELETE product name by  setting is_deleted field in Database as TRUE
    def delete(self,product_name):
        item = ProductModel.find_by_name(product_name)
        if item:
            item.is_deleted = True
            item.save_to_db()
            return {'message':'Product deleted.'},200

        return {'message':'Product not found.'},404

    # update quantity of product
    def put(self,product_name):
        item = ProductModel.find_by_name(product_name)
        parser = reqparse.RequestParser()
        parser.add_argument('quantity',
                            type=int,
                            required=True,
                            help="Quantity cannot be left blank!"
                            )
        if item:
            data = parser.parse_args()
            item.quantity = data['quantity']
            item.save_to_db()
            return {'message':f'Quantity of Product:{product_name} updated to {item.quantity}'}

        return {'message':'Product name not found'},404


# fetch all the products stored in database
class Products(Resource):
    def get(self):
        return {'items':list(map(lambda x:x.json(),ProductModel.query.all()))}


class Category(Resource):
    def get(self,category_name):
        data=ProductModel.find_by_product_category(category_name)
        if data:
            return {'items':list(map(lambda x:x.json(),data.all()))},200

        return {"message","Enter category"},404
