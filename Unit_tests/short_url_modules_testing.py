import unittest
import sys
# this line make Backend folder accessable
sys.path.insert(0, '/root/Shorten_URL-s')
import Backend.short_url_modules as sh

class TestShortUrl(unittest.TestCase):
    def setUp(self):
        self.short_url = sh.ShortUrl()

    def test_get_domain_name(self):
        original_url = "https://www.youtube.com/watch?v=_fLgknT8Hh"
        domain_name = self.short_url.get_domain_name(original_url)
        self.assertEqual(domain_name, "youtube")

    def test_get_domain_name_fail(self):
        original_url = "https://www.youtube.com/watch?v=_fLgknT8Hh"
        domain_name = self.short_url.get_domain_name(original_url)
        self.assertNotEqual(domain_name, "example")

    def test_get_shorten_url(self):
        original_url = "https://www.youtube.com/watch?v=_fLgknT8Hh"
        shortened_url = self.short_url.get_shorten_url(original_url)
        self.assertEqual(len(shortened_url.split("/")[-1]), 6)
    
    def test_get_shorten_url_fail(self):
        original_url = "https://www.youtube.com/watch?v=_fLgknT8Hh"
        shortened_url = self.short_url.get_shorten_url(original_url)
        self.assertNotEqual(len(shortened_url.split("/")[-1]), 10)

if __name__ == '__main__':
    unittest.main()
