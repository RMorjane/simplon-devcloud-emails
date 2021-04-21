import unittest
from jobs_scraper import JobScraper

class TestJobScraper(unittest.TestCase):

    def test_read_links(self):
        js = JobScraper()
        js.read_pages()
        list_pages = js.list_pages
        self.assertFalse(len(list_pages)==0)

if __name__ == '__main__':
    unittest.main()