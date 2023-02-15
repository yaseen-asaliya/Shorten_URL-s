import unittest
import unittest.mock
import Backend.database_configaration as dbc
from unittest.mock import Mock, patch

class TestDatabaseConfigration(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = Mock()
        self.mock_conn = Mock()
        self.mock_conn.cursor.return_value = self.mock_cursor

        self.database = dbc.DatabaseConfigraton()
        self.database.cursor = self.mock_cursor
        self.database.connection = self.mock_conn
        
        self.original_url = "https://mail.google.com/mail/u/0/#inbox"
        self.shorten_url = "http://google.com/rgEF3S"
        
    def test_init(self):
       self.assertIsNotNone(self.database.connection)
       self.assertIsNotNone(self.database.cursor)
       
    def test_setup_database_tables(self):
        self.database.create_table_in_db()

        self.mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS url (time TIMESTAMP, original_url TEXT, shorten_url TEXT);")
        self.mock_conn.commit.assert_called_once()

    def test_insert_url(self):
        self.mock_cursor.fetchone.return_value = (self.shorten_url,)

        short_url = self.database.insert_url(self.original_url)
        self.assertEqual(len(short_url.split("/")[-1]), 6)
    
    def test_get_full_url(self):
        result = self.database.get_full_url(self.shorten_url)
        self.assertIsNotNone(result)
        
    def test_get_shorten_url(self):
        result = self.database.get_shorten_url(self.original_url)
        self.assertIsNotNone(result)
        
    def test_check_original_url_if_exsist(self):
        self.assertTrue(self.database.check_original_url_if_exsist(self.original_url))
    
    def test_get_all_urls(self):
        sample_data = [(self.original_url, self.shorten_url, '2023-02-13 12:34:56')]
        self.mock_cursor.fetchall.return_value = sample_data
        
        result = self.database.get_all_urls("2023-02-13","mail",1,3)
        self.assertIn("original_url", result[0])
        self.assertEqual(len(result[0]), 3)
        
        
if __name__ == '__main__':
    unittest.main()
