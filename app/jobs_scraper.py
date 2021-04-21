import requests
import pprint
from bs4 import BeautifulSoup
import logging    
from logging.handlers import RotatingFileHandler

class JobScraperItem:

    def __init__(self,job_url):
        self.job_url = job_url
        self.job_title = ""
        self.job_company = ""
        self.job_contact = ""
        self.published_date = ""
        self.start_date = ""
        self.job_type = ""
        self.job_salary = ""
        self.job_skills = ""

    def read_infos(self):

        response = requests.get(self.job_url)
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(response.content, from_encoding=encoding,features="html.parser")

        self.job_title = soup.find("div",{"class": "job-item-title title"}).text.strip()

        array_company = soup.find("div",{"class": "job-item-company"}).findChildren()
        if len(array_company)>0:
            self.job_company = array_company[1].text.strip()

        array_published_date = soup.find("div",{"class": "job-item-date"}).findChildren()
        if len(array_published_date)>0:
            self.published_date = array_published_date[1].text.strip()

        array_start_date = soup.find("div",{"class": "job-item-start"}).findChildren()
        if len(array_start_date)>0:
            self.start_date = array_start_date[1].text.strip()

        array_salary = soup.find("div",{"class": "job-item-payment"}).findChildren()
        if len(array_salary)>0:
            self.job_salary = array_salary[1].text.strip()

        array_skills = soup.find("div",{"class": "job-item-competencies"}).findChildren()
        if len(array_skills)>0:
            self.job_skills = array_skills[1].text.strip()

        self.job_type = soup.find("li",{"class": "job-item-offer-item"}).text.strip()

        list_a = soup.find_all("a")
        for loop_a in list_a:
            href = loop_a["href"].strip()
            if href[0:7] == "mailto:":
                self.job_contact = href[7:len(loop_a["href"])]        

class JobScraperPage:

    def __init__(self,page):
        self.page = page
        self.url_page = "https://www.frenchtechbordeaux.com/job/?sf_paged="+str(page)
        self.list_hrefs = []
        self.json_page = {}

    def read_links(self):
        response = requests.get(self.url_page)
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(response.content, from_encoding=encoding,features="html.parser")
        links = soup.find_all("a",{"class": "single-block-item"})
        self.list_hrefs = [loop_link["href"].strip() for loop_link in links]
        self.json_page["page"] = self.page
        self.json_page["url_page"] = self.url_page
        self.json_page["hrefs"] = self.list_hrefs

class JobScraper:

    def __init__(self):
        self.list_pages = []

    def read_pages(self):
        i = 1
        while True:
            jsp = JobScraperPage(i)
            jsp.read_links()
            if len(jsp.list_hrefs)==0:
                break
            else:
                self.list_pages.append(jsp.json_page)
                i += 1