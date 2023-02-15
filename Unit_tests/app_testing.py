import unittest
import json
import sys
# this line make app class accessable
sys.path.insert(0, '/root/Shorten_URL-s')
import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_get_shorten_url(self):
        data = {"url": "https://mail.google.com/mail/u/0/#inbox"}
        response = self.app.post("/shorten_url", data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("shortened_url", data)

    def test_get_original_url(self):
        response = self.app.get("/original_url", data=json.dumps({'url': "https://mail.google/t5xUjL"}), content_type='application/json')
        self.assertEqual(response.status_code, 302) 
    
    def test_get_all_urls(self):
       response = self.app.get("/urls?date=2022-02-13&search=google&page=1&per_page=3")
       data = json.loads(response.data)
       self.assertEqual(response.status_code, 200)
       self.assertIn("urls", data)
       self.assertIsInstance(data["urls"], list)
       
    def test_get_shorten_url_fail(self):
       data = {"sssss": "https://mail.google.com/mail/u/0/#inbox"}
       response = self.app.post("/shorten_url", data=json.dumps(data))
       self.assertNotEqual(response.status_code, 200) 
       
    def test_get_original_url_fail(self):
        response = self.app.get("/original_url", data=json.dumps({'ssad': 'https://mail.google/E5wU2D'}), content_type='application/json')
        self.assertNotEqual(response.status_code, 200)
        
    def test_get_all_urls_fail(self):
        response = self.app.get("/urlss?invalid_key=2022-02-13&search=google&page=1&per_page=3")
        self.assertNotEqual(response.status_code, 200) 

if __name__ == "__main__":
    unittest.main()
