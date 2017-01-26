from flask import json
import unittest
from tests import BaseTest


class TestAuth(BaseTest):

    '''Tests the authorization of the users'''

    def test_register_successfully(self):

        '''Tests for a successful registration'''

        self.user = {"username": "pineapple",
                                 "password": "fruit1"}
        response = self.client.post('/auth/register', data=json.dumps(self.user), content_type="application/json")
        message = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('created user', message['message'])

    def test_register_unsuccessfully(self):

        self.user = {"username": "Kenyan",
                                 "password": "fruit1"}
        response = self.client.post('/auth/register', data=json.dumps(self.user), content_type="application/json")
        message = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Username already exists', message['message'])

    def test_login_successfully(self):
        self.user = {"username": "Kenyan",
                                 "password": "kicc123"}
        response = self.client.post('/auth/login', data=json.dumps(self.user), content_type="application/json")
        message = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', message)

    def test_login_without_password(self):
        self.user = {"username": "Kenyan",
                                 "password": ""}
        response = self.client.post('/auth/login', data=json.dumps(self.user), content_type="application/json")
        message = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Need username and password to login', message['message'])

    def test_login_with_wrong_credentials(self):
        self.user = {"username": "kenyan",
                                 "password": "kicc345"}
        response = self.client.post('/auth/login', data=json.dumps(self.user), content_type="application/json")
        message = json.loads(response.data)
        self.assertEqual(response.status_code, 406)
        self.assertIn('Username or password is invalid.', message['message'])



