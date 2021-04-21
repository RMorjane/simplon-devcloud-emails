import os
import psycopg2
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
load_dotenv('.env')

class JobsPostgres:

    SECRET_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    HOST_VM = os.getenv("AZURE_HOST_VM")

    def __init__(self):
        self.connection = None
        self.logger = None
        self.list_jobs = []

    def connect(self):
        try:
            host = "localhost"
            user = "postgres"
            dbname = "postgres"
            password = "postgres"
            port = "5432"
            cnt_string = "host={0} user={1} dbname={2} password={3} port={4} sslmode='require'".format(host,user,dbname,password,port)
            self.connection = psycopg2.connect(cnt_string)
            print("Connexion réussie : " + str(self.connection))
            return True
        except (Exception, psycopg2.Error) as error:
            print("Impossible de se connecter au serveur postgres : " + str(error))
            return False

    def create_table(self):
        try:
            with self.connection.cursor() as my_cursor:
                sql_create_table = """
                CREATE TABLE IF NOT EXISTS job(
                job_url VARCHAR NOT NULL PRIMARY KEY,
                job_title VARCHAR(100) NOT NULL,
                job_type VARCHAR(100),
                job_company VARCHAR(100) NOT NULL,
                job_contact VARCHAR(100) NOT NULL,
                published_date VARCHAR(100),
                start_date VARCHAR(100),
                job_salary VARCHAR,
                job_skills VARCHAR);
                """
                my_cursor.execute(sql_create_table)
                self.connection.commit()
                my_cursor.close()
                self.logger.info("Création de la table réussie")
                return True
        except (Exception, psycopg2.Error) as error:
            self.logger.error("Impossible de créer la table dans la base postgres : " + str(error))
            return False

    def add_job(self,job_item):
        if not self.job_exists(job_item.job_url):
            try:
                with self.connection.cursor() as my_cursor:
                    sql_add_job = """INSERT INTO job(job_url,job_title,job_type,job_company,job_contact,
                    published_date,start_date,job_salary,job_skills)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    my_cursor.execute(sql_add_job,(
                        job_item.job_url,
                        job_item.job_title.replace("'","\\'"),
                        job_item.job_type.replace("'","\\'"),
                        job_item.job_company.replace("'","\\'"),
                        job_item.job_contact.replace("'","\\'"),
                        job_item.published_date.replace("'","\\'"),
                        job_item.start_date.replace("'","\\'"),
                        job_item.job_salary.replace("'","\\'"),
                        job_item.job_skills.replace("'","\\'"))
                    )
                    self.connection.commit()
                    my_cursor.close()
                    self.logger.info("Inssertion réussie")
            except (Exception, psycopg2.Error) as error:
                self.logger.error("Impossible d'ajouter un job dans la base postgres : " + str(error))
        else:
            self.logger.info("Offre d'emploi déjà enregistré dans la base postgres")

    def job_exists(self,job_url):
        try:
            with self.connection.cursor() as my_cursor:
                sql_job_exists = "SELECT job_url FROM job WHERE job_url=%s"
                my_cursor.execute(sql_job_exists,(job_url,))
                exists = len(my_cursor.fetchall())>0
                my_cursor.close()
                return exists
        except (Exception, psycopg2.Error) as error:
             self.logger.error("Erreur dans la requette de selection des offres : " + str(error))
             return False

    def find_jobs(self, job_dict={},limit=0):
        list_keys = []
        list_values = []
        list_args = ()
        for key, value in job_dict.items():
            list_keys.append(key)
            list_values.append(value)
        try:
            with self.connection.cursor() as my_cursor:
                sql_find_jobs = "SELECT * FROM job"
                for i in range(len(list_keys)):
                    if i == 0:
                        sql_find_jobs += " WHERE "
                    else:
                        sql_find_jobs += " AND "
                    if type(list_values[i]) == str:
                        list_args = (list_args + ("%"+list_values[i]+"%",))
                        sql_find_jobs += list_keys[i] + " LIKE '%s'"
                    elif type(list_values[i]) == int:
                        list_args = (list_args + (list_values[i],))
                        sql_find_jobs += list_keys[i] + "=%s"
                if limit>0:
                    list_args = (list_args +(limit,))
                    sql_find_jobs += " LIMIT %s;"
                print(sql_find_jobs)
                my_cursor.execute(sql_find_jobs % (list_args))
                self.list_jobs = []
                for loop_job in my_cursor.fetchall():
                    self.list_jobs.append({
                        "job_url": loop_job[0],
                        "job_title": loop_job[1],
                        "job_type": loop_job[2],
                        "job_company": loop_job[3],
                        "job_contact": loop_job[4],
                        "published_date": loop_job[5],
                        "start_date": loop_job[6],
                        "job_salary": loop_job[7],
                        "job_skills": loop_job[8]
                    })
                my_cursor.close()
                self.logger.info("Successfull : Jobs were founded")
                return True
        except (Exception, psycopg2.Error) as error:
            self.logger.error("Erreur dans la requête de selection des offres : "+str(error))
            return False

    def set_logger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = RotatingFileHandler('log.txt', 'a', 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)