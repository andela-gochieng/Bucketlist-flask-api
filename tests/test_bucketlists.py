import json 
from tests import BaseTest

class TestBucketlists(BaseTest):

  def test_create_bucketlist(self):
    self.bucketlist = {'name': 'Do Today'}
    response = self.app.post('/bucketlists/', data=self.bucketlist)
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 201)
    self.assertIn('Bucketlist Do Today created', message['msg'])

  def test_create_duplicate_bucketlist(self):
    self.bucketlist = {'name': 'Before End Of Year'}
    response = self.app.post('/bucketlists/', data=self.bucketlist)
    self.bucketlist = {'name': 'Before End Of Year'}
    response = self.app.post('/bucketlists/', data=self.bucketlist)
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 400)
    self.assertIn('Bucketlist name already exists', message['msg'])

  def test_get_specific_bucketlist(self):
    self.bucketlist_id = 1
    response = self.app.get('/bucketlists/{}'.format(self.bucketlist_id))
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual('Does Not Exist', message['msg'])

  def test_get_nonexistent_bucketlist(self):
    self.bucket_list.id = 2
    response = self.app.get('/bucketlists/1/')
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual('Restaurants To Visit', message['name'])

  def test_get_all_bucketlists(self):
    response = self.app.get('/bucketlists/')
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual('Restaurants To Visit', message['name'])

  def test_get_nonexistent_bucketlists(self):
    self.user = {"username": "pineapple",
                                 "password": "fruit1"}
    response = self.app.post('/auth/register/', data=self.user)
    response = self.app.post('/auth/login/', data=self.user)
    response = self.app.post('/bucketlists/')
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 400)
    self.assertEqual('No bucketlists to display', message['msg'])


  def test_edit_existing_bucketlist(self):
    self.bucketlist_id = 1
    self.new_name = {'name': 'Restaurants'}
    response = self.app.put('/bucketlists/{}' .format(self.bucketlist_id),
                            data=self.new_name) 
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 201)
    self.assertEqual('Restaurants', message['name'])


  def test_delete_existing_bucketlist(self):
    self.bucketlist_id = 1
    response = self.app.delete('/bucketlists/{}' .format(self.bucketlist_id))
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual('Restaurants To Visit has been deleted', message['msg'])

  def test_add_item(self):
    self.item = {'name': 'Sankara', 'Bucketlist_id': '1'}
    response = self.app.post('/bucketlists/1/items/', data=self.item)
    self.assertEqual(response.status_code, 200)

  def test_add_item_to_nonexistent_bucketlist(self):
    self.item = {'name': 'Sankara', 'bucketlist_id': '2'}
    response = self.app.post('/bucketlists/2/items/', data=self.item)
    self.assertEqual(response.status_code, 404)

  def  test_add_item_without_name(self):
    self.item = {'name': '', 'Bucketlist_id': '1'}
    response = self.app.post('/bucketlists/1/items/', data=self.item)
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 400)
    self.assertEqual('No name given', message['msg'])

  def test_update_item(self):
    self.new_name = {'name': 'Sankara', 'bucketlist_id':1}
    response = self.app.put('/bucketlists/1/items/1', data=self.new_name)
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual('Sankara', message['name'])

  def test_update_nonexistent_item(self):
    self.new_name = {'name': 'Sankara', 'bucketlist_id':1}
    response = self.app.put('/bucketlists/1/items/3', data=self.new_name)
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 404)
    self.assertEqual('Item Not Found', message['msg'])

  def test_delete_item(self):
    response = self.app.delete('/bucketlists/1/items/2', data=self.new_name)
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual('Item deleted', message['msg'])

  def test_delete_nonexistent_item(self):
    response = self.app.delete('/bucketlists/1/items/2', data=self.new_name)
    message = json.loads(response.data)
    self.assertEqual(response.status_code, 404)
    self.assertEqual('Item deleted', message['msg'])






  

