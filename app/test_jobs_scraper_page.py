import unittest
from jobs_scraper import JobScraperPage

class TestJobScraper(unittest.TestCase):

    def test_read_links(self):
        js = JobScraperPage(1)
        js.read_links()
        list_hrefs = js.list_hrefs
        self.assertFalse(len(list_hrefs)==0)

if __name__ == '__main__':
    unittest.main()