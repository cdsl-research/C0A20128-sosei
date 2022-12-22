import base64
from locust import HttpUser, task
from random import randint, choice


class WebTasks(HttpUser):

    @task
    def load(self):
        base64string = base64.b64encode(('%s:%s' % ('user', 'password')).encode()).decode()

        catalogue = self.client.get("/catalogue").json()

        ## delete Holy
        count = 0
        for dic in catalogue:
            if dic['name'] == 'Holy':
                catalogue.pop(count)
            count += 1

        category_item = choice(catalogue)
        item_id = category_item["id"]

        self.client.get("/")
        self.client.get("/login", headers={"Authorization":"Basic %s" % base64string})
        self.client.get("/category.html")
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})