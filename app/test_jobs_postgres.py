import unittest
from unittest.mock import MagicMock
from jobs_postgres import JobsPostgres

class TestJobPostgres(unittest.TestCase):

    jobs_db = JobsPostgres()

    # def test_connect(self):
    #     TestJobPostgres.jobs_db.set_logger()
    #     self.assertTrue(TestJobPostgres.jobs_db.connect())

    def mock_test_connect(self):
        mock = MagicMock(spec=JobsPostgres)
        connected = mock.connect.return_value
        self.assertTrue(connected)

    # def test_create_tables(self):
    #     self.assertTrue(TestJobPostgres.jobs_db.create_table())

if __name__ == '__main__':
    unittest.main()