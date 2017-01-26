import json
import unittest
from tests import BaseTest
from app.models import User, Bucketlist, Item, db


class TestBucketlists(BaseTest):
    def login(self):
        self.user = db.session.query(User).filter_by(username="Kenyan").first()
        self.token = self.user.generate_auth_token().decode("utf-8")

    def test_create_bucketlist(self):
        self.login()
        bucketlist = {'name': 'Do Today'}
        response = self.client.post('/bucketlists',
                                    data=json.dumps(bucketlist),
                                    headers={"Authorization": "Bearer {}".
                                             format(self.token)},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_create_duplicate_bucketlist(self):
        self.login()
        bucketlist = {'name': 'Restaurants to visit'}
        response = self.client.post('/bucketlists/', data=json.dumps(bucketlist),
                                    headers={"Authorization": "Bearer {}".
                                             format(self.token)},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 405)

    def test_get_specific_bucketlist(self):
        self.login()
        response = self.client.get('/bucketlists/1', headers={
                                   "Authorization": "Bearer {}".
                                   format(self.token)},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_bucketlist(self):
        self.login()
        response = self.client.get('/bucketlists/2', headers={
                                   "Authorization": "Bearer {}".
                                   format(self.token)},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_get_all_bucketlists(self):
        self.login()
        response = self.client.get('/bucketlists/', headers={"Authorization":
                                                             "Bearer {}".format(self.token)},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_bucketlists(self):
        self.user = {"username": "pineapple",
                     "password": "fruit1"}
        response = self.client.post(
            '/auth/register/', data=json.dumps(self.user))
        response = self.client.post('/auth/login/', data=json.dumps(self.user))
        response = self.client.post('/bucketlists/')
        self.assertEqual(response.status_code, 405)

    def test_edit_existing_bucketlist(self):
        self.login()
        self.new_name = {'name': 'Restaurants'}
        response = self.client.put('/bucketlists/1',
                                   data=json.dumps(self.new_name), headers={
                                       "Authorization":
                                       "Bearer {}".format(self.token)},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 202)

    def test_delete_existing_bucketlist(self):
        self.login()
        response = self.client.delete('/bucketlists/1', headers={
            "Authorization":
            "Bearer {}".format(self.token)},
            content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_add_item(self):
        self.login()
        self.item = {'name': 'Sankara'}
        response = self.client.post('/bucketlists/1/items',
                                    data=json.dumps(self.item), headers={
                                        "Authorization":
                                        "Bearer {}".format(self.token)},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_add_item_to_nonexistent_bucketlist(self):
        self.login()
        self.item = {'name': 'Sankara'}
        response = self.client.post('/bucketlists/3/items',
                                    data=json.dumps(self.item), headers={
                                        "Authorization":
                                        "Bearer {}".format(self.token)},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_add_item_without_name(self):
        self.login()
        self.item = {'name': ''}
        response = self.client.post('/bucketlists/1/items',
                                    data=json.dumps(self.item), headers={
                                        "Authorization":
                                        "Bearer {}".format(self.token)},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_update_item(self):
        self.login()
        new_name = {'name': 'Sankara', 'done': 'true'}
        response = self.client.put('/bucketlists/1/items/1',
                                   data=json.dumps(new_name), headers={
                                       "Authorization":
                                       "Bearer {}".format(self.token)},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 202)

    def test_update_nonexistent_item(self):
        self.login()
        new_name = {'name': 'Sankara', 'done': 'true'}
        response = self.client.put('/bucketlists/1/items/3',
                                   data=json.dumps(new_name), headers={
                                       "Authorization":
                                       "Bearer {}".format(self.token)},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_item(self):
        self.login()
        response = self.client.delete('/bucketlists/1/items/2',
                                      headers={
                                          "Authorization":
                                          "Bearer {}".format(self.token)},
                                      content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_nonexistent_item(self):
        self.login()
        response = self.client.delete('/bucketlists/1/items/3',
                                      headers={
                                          "Authorization":
                                          "Bearer {}".format(self.token)},
                                      content_type="application/json")
        self.assertEqual(response.status_code, 404)
