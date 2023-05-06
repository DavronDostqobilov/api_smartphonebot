from tinydb import TinyDB, Query
import requests

class Cart:
    def __init__(self):
        self.base_url = "https://davron0703qwerty1234.pythonanywhere.com"


    def add(self, brend, doc_id, chat_id):
        """
        add card
        data = {
            'brand':brand,
            'doc_id': doc_id,
            chat_id: chat_id
            }
        """
        data = {
            'company':brend,
            'product_id': doc_id,
            'chat_id': chat_id
        }
        url = f"{self.base_url}/smartphone/add"
        r = requests.post(url, json=data)
        return r

    def get_cart(self, chat_id):
        r = requests.get(self.base_url + "/smartphone/getorder/" +f"{chat_id}" )
        data=r.json()
        #print(data['get_order'])
        return data['get_order']
    
    def remove(self, chat_id):
        data={"chat_id": chat_id}
        url = f"{self.base_url}/smartphone/clearorder"
        print(url)
        r = requests.post(url, json=data)
        print(r)
        return r
        