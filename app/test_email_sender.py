import unittest
from unittest.mock import MagicMock
from email_sender import EmailSender

class TestEmailSender(unittest.TestCase):

    def test_send_mail(self):
        smtp = MagicMock()
        smtplib.SMTP_SSL = smtp
        with patch('module.SMTP') as smtp:
            self.assertIs(smtp)
        
if __name__=="__main__":
    unittest.main()