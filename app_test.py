import unittest
import requests


class AppTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000"
    PRODUCT_URL = "{}/product".format(API_URL)
    PRODUCT_NAME = "item3"
    PRODUCT_OBJ = {
        "price":10,
        "quantity":10,
        "product_category":"cookies",
        "exp_date":"2021-01-01 09:30:50",
        "manufacturing_date":"2020-07-01 09:30:50"
    }
    UPDATE_QTY = {
        "quantity":10
    }
    USER_OBJ = {
        "username":"admin",
        "password":"admin"
    }

    def test_1_user_register(self):
        r = requests.post("{}/register".format(AppTest.API_URL),json=AppTest.USER_OBJ)
        self.assertEqual(r.status_code,201)

    def test_2_user_login(self):
        r = requests.post("{}/login".format(AppTest.API_URL),json=AppTest.USER_OBJ)
        self.assertEqual(r.status_code,200)

    def test_3_invalid_user_login(self):
        r = requests.post("{}/login".format(AppTest.API_URL),json={"username":"abc","password":"321"})
        self.assertEqual(r.status_code,401)

    def test_4_add_item(self):
        r = requests.post("{}/{}".format(AppTest.PRODUCT_URL,AppTest.PRODUCT_NAME),json=AppTest.PRODUCT_OBJ)
        self.assertEqual(r.status_code,201)

    def test_5_search_item(self):
        r = requests.get("{}/{}".format(AppTest.PRODUCT_URL,AppTest.PRODUCT_NAME))
        self.assertEqual(r.status_code,200)

    def test_6_delete_item(self):
        r = requests.delete("{}/{}".format(AppTest.PRODUCT_URL,AppTest.PRODUCT_NAME))
        self.assertEqual(r.status_code,200)

    def test_7_update_qty(self):
        r = requests.delete("{}/{}".format(AppTest.PRODUCT_URL,AppTest.PRODUCT_NAME),json=AppTest.UPDATE_QTY)
        self.assertEqual(r.status_code,200)

    def test_8_get_all_items(self):
        r = requests.get("{}/products".format(AppTest.API_URL))
        self.assertEqual(r.status_code,200)

    def test_9_get_user(self):
        r = requests.get("{}/user/{}".format(AppTest.API_URL,AppTest.USER_OBJ["username"]),json=AppTest.USER_OBJ)
        self.assertEqual(r.status_code,200)

    def test_10_delete_user(self):
        r = requests.delete("{}/user/{}".format(AppTest.API_URL,AppTest.USER_OBJ["username"]),json=AppTest.USER_OBJ)
        self.assertEqual(r.status_code,200)
