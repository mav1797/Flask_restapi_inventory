from db import db
from datetime import datetime
from pytz import timezone


class ProductModel(db.Model):
    # table and column
    __tablename__ = 'items'
    id = db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String(80))
    product_category = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    quantity = db.Column(db.Integer)
    exp_date = db.Column(db.DateTime)
    manufacturing_time = db.Column(db.DateTime)
    is_deleted = db.Column(db.Boolean,default=False)

    # product_img=img

    def __init__(self,product_name,product_category,price,quantity,exp_date,manufacturing_time):
        self.product_name = product_name
        self.product_category = product_category
        self.price = price
        self.quantity = quantity
        self.exp_date = exp_date
        self.manufacturing_time = manufacturing_time

    def json(self):
        return {'product_id':self.id,'product_name':self.product_name,'product_category':self.product_category,
                'price':self.price,'quantity':self.quantity,'exp_date':str(self.exp_date),
                'manufacturing_time':str(self.manufacturing_time),'is_deleted':self.is_deleted}

    # find product by name
    @classmethod
    def find_by_name(cls,product_name):
        return cls.query.filter_by(product_name=product_name).first()

    @classmethod
    def find_by_product_category(cls,product_category):
        return cls.query.filter_by(product_category=product_category)

    # save changes / new data to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # convert any time to CST time
    @classmethod
    def convert_to_cst_time(cls,date):
        central_time = timezone('US/Central')
        if type(date)==str:
            date = datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
        cst_time = date.astimezone(central_time)
        new_time = cst_time.replace(tzinfo=None)
        return new_time
