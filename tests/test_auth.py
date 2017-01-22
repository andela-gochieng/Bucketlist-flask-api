import json
from tests import BaseTest


class TestAuth(BaseTest):

    '''Tests the authorization of the users'''

    def test_home(self):
        '''Tests the response from the home index'''
        response = self.app.get('/')
        feedback = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to Achieve! Register or login to continue',
                      feedback)

    def test_register_successfully(self):

        '''Tests for a successful registration'''

        self.user = {"username": "pineapple",
                                 "password": "fruit1"}
        response = self.app.post('/auth/register/', data=self.user)
        message = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('login now to continue', message['msg'])

    def test_register_unsuccessfully(self):
        self.user = {"username": "pineapple",
                                 "password": "fruit1"}
        self.app.post('/auth/register/', data=self.user)
        
        self.user = {"username": "pineapple",
                                 "password": "fruit1"}
        response = self.app.post('/auth/register/', data=self.user)
        message = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('username already exists', message['msg'])

    def test_login_successfully(self):
        self.user = {"username": "pineapple",
                                 "password": "fruit1"}
        response = self.app.post('/auth/login/', data=self.user)
        message = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully logged in', message['msg'])

    def test_login_without_password(self):
        self.user = {"username": "pineapple",
                                 "password": ""}
        response = self.app.post('/auth/login/', data=self.user)
        message = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('no password provided', message['msg'])

    def test_login_with_wrong_credentials(self):
        self.user = {"username": "kenyan",
                                 "password": "kicc345"}
        response = self.app.post('/auth/login/', data=self.user)
        message = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('wrong username or password provided', message['msg'])



