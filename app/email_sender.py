import os
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv('.env')

class EmailSender:

    def __init__(self):
        self.email_sender = "rhellabmorjane@gmail.com"
        self.password = os.getenv("EMAIL_PASSWORD")
        self.email_receiver = ""
        self.smtp_address = "smtp.gmail.com"
        self.subject_message = "Offres d'emploi Dev Cloud"
        self.smtp_port = 465
        self.html_message = {}

    def create_html_message(self,email_receiver,list_jobs={}):
        self.email_receiver = email_receiver
        self.html_message = MIMEMultipart('alternative')
        self.html_message['Subject'] = self.subject_message
        self.html_message['From'] = self.email_sender
        self.html_message['To'] = self.email_receiver
        html = """\
        <html>
              <head></head>
              <body>
                    <h1>Liste des 5 dernières offres d'emploi :</h1>
                    <p>
        """
        if type(list_jobs) == list:
            for loop_job in list_jobs:
                html += loop_job["job_url"] + "<br>"
                html += loop_job["job_title"] + "<br>"
                html += loop_job["job_type"] + "<br>"
                html += loop_job["job_company"] + "<br>"
                html += loop_job["job_contact"] + "<br>"
                html += loop_job["published_date"] + "<br>"
                html += loop_job["start_date"] + "<br>"
                html += loop_job["job_salary"] + "<br>"
                html += loop_job["job_skills"] + "<br>"
                html += "<hr>"
        html += """</p>
              </body>
        </html>
        """
        self.html_message.attach(MIMEText(html, 'html'))

    def send_mail(self):
        #local_smtp = smtplib.SMTP_SSL
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_address, self.smtp_port, context=context) as server:
                server.login(self.email_sender, self.password)
                server.sendmail(self.email_sender, self.email_receiver, self.html_message.as_string())
                #local_smtp = server
                server.quit()
                print("Le mail a été envoyé avec succès !!!")
                return True
        except:
            print("Erreur lors de l'envoie du mail !!!")
            return False
        #return local_smtp