import pprint
from jobs_scraper import JobScraper, JobScraperItem
from jobs_postgres import JobsPostgres
from email_sender import EmailSender
from flask import Flask, render_template, request

import logging

logging.basicConfig(filename='logs.log', level=logging.DEBUG)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def welcome():
    return render_template("index.html")

@app.route("/response/", methods=['POST'])
def response():

    result = {}
    email = request.form.get("email")

    js = JobScraper()
    js.read_pages()
    list_pages = js.list_pages

    jobs = JobsPostgres()
    jobs.set_logger()

    state = jobs.connect() and jobs.create_table()

    if state:

        for loop_page in list_pages:
            for loop_href in loop_page["hrefs"]:
                job_item = JobScraperItem(loop_href)
                job_item.read_infos()
                jobs.add_job(job_item)

        state &= jobs.find_jobs({},5)
        pprint.pprint(jobs.list_jobs)
        jobs.connection.close()

        sender = EmailSender()
        sender.create_html_message(email,jobs.list_jobs)
        state &= sender.send_mail()

    if state:
        result["text"] = "Succes"
        result["color"] = "green"
    else:
        result["text"] = "Failed"
        result["color"] = "red"
    
    return render_template("response.html",result = result)

if __name__=="__main__":

    app.run(host="0.0.0.0", port=3000, debug=True)