import unittest
import json
from app import app, mongodb

class APITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a testing client and a fresh database for tests."""
        cls.app = app
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True
        
        # Drop the database and create the collection before tests
        mongodb.db.drop_collection('users')
        mongodb.db.create_collection('users')

    def setUp(self):
        """Reset the state before each test."""
        self.user_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "age": 30
        }
        
        # Insert a test user
        mongodb.db.users.insert_one(self.user_data)

    def tearDown(self):
        """Remove all users after each test."""
        mongodb.db.users.delete_many({})

    def test_get_users(self):
        """Test the GET /users endpoint."""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    def test_get_user_by_id(self):
        """Test the GET /users/<user_id> endpoint."""
        user = mongodb.db.users.find_one({'name': 'John Doe'})
        user_id = str(user['_id'])
        
        response = self.client.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    def test_get_user_by_email(self):
        """Test the GET /users/email/<email> endpoint."""
        response = self.client.get('/users/email/john.doe@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    def test_update_user_by_id(self):
        """Test the PUT /users/<user_id> endpoint."""
        user = mongodb.db.users.find_one({'name': 'John Doe'})
        user_id = str(user['_id'])
        
        updated_data = {"name": "Jane Doe", "email": "jane.doe@example.com", "age": 25}
        response = self.client.put(f'/users/{user_id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Verify the user was updated
        updated_user = mongodb.db.users.find_one({'_id': user['_id']})
        self.assertEqual(updated_user['name'], "Jane Doe")

    def test_delete_user_by_id(self):
        """Test the DELETE /users/<user_id> endpoint."""
        user = mongodb.db.users.find_one({'name': 'John Doe'})
        user_id = str(user['_id'])
        
        response = self.client.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)

        # Verify the user was deleted
        deleted_user = mongodb.db.users.find_one({'_id': user['_id']})
        self.assertIsNone(deleted_user)

    def test_invalid_user_id(self):
        """Test the GET /users/<user_id> endpoint with an invalid ID."""
        response = self.client.get('/users/invalid_id')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid ID', response.data)

if __name__ == '__main__':
    unittest.main()
