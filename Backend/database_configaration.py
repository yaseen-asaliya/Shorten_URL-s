import logging
import datetime
import Backend.short_url_modules as sh
from Backend.logger import log_action
import mysql.connector
from dotenv import load_dotenv
import os

class DatabaseConfigraton:
    @log_action
    def __init__(self):
        try:
            logging.debug("Connecting to the database.")
            load_dotenv()
            self.connection = mysql.connector.connect(host=os.getenv("DB_HOST"),user=os.getenv("DB_USER"), passwd=os.getenv("DB_PASS"), database=os.getenv("DB_NAME"), port=os.getenv("DB_PORT"))
            self.cursor = self.connection.cursor()
            logging.info("Database connected successfully.")
            self.create_table_in_db()

        except Exception as err:
            logging.error(f"An error occurred while connecting to the database: {err}")

    @log_action
    def create_table_in_db(self):
        try:
            logging.debug("Creating tables in database...")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS url (time TIMESTAMP, original_url TEXT, shorten_url TEXT);")
            logging.info("Table URL created successfully.")
            self.connection.commit()
        except Exception as err:
            logging.error(f"Error setting up database tables: {err}")

    @log_action
    def get_unique_url(self, original_url):
        try:
            logging.debug("Geanrating unique url")
            self.cursor.execute("SELECT shorten_url FROM url")
            urls = self.cursor.fetchall()

            while True:
                short_url = sh.get_shorten_url(original_url)
                unique=True
                for url in urls:
                    if (url[-6:] == short_url[-6:]):
                        unique=False

                if unique:
                   return short_url

        except Exception as err:
            logging.error(f"Error while inserting data in table: {err}")

    @log_action
    def insert_url(self, original_url):
        try:
            short_url =  self.get_unique_url(original_url)
            logging.debug(f"Inserting {short_url} into urls table...")
            self.cursor.execute("INSERT INTO url (time, original_url, shorten_url) VALUES (%s,%s,%s)",
                                (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), original_url, short_url))
            self.connection.commit()
            logging.info("Inserting done successfully.")
            return short_url

        except Exception as err:
            logging.error(f"Error while inserting data in table: {err}")
            return "non"

    @log_action
    def get_full_url(self, short_url):
        self.cursor.execute("SELECT original_url FROM url WHERE shorten_url=%s", (short_url,))
        logging.debug("Selecting original_url from database...")
        return self.cursor.fetchone()

    @log_action
    def get_shorten_url(self, original_url):
        self.cursor.execute("SELECT shorten_url FROM url WHERE original_url=%s", (original_url,))
        logging.debug("Selecting shorten_url from database...")
        return self.cursor.fetchone()

    @log_action
    def check_original_url_if_exsist(self, original_url):
        logging.info(f"checking if the url {original_url} is exist")
        self.cursor.execute("SELECT original_url FROM url WHERE original_url=%s", (original_url,))
        if self.cursor.fetchone():
            return True
        return False

    @log_action
    def get_all_urls(self, date, search, page, per_page):
        query = "SELECT time, original_url, shorten_url FROM url"
        params = []

        if date and search:
            query += " WHERE time LIKE %s AND original_url LIKE %s"
            params.append(date + "%")
            params.append("%" + search + "%")
        else:
            if date:
               query += " WHERE time LIKE %s"
               params.append(date + "%")

            if search:
                query += " WHERE original_url LIKE %s"
                params.append("%" + search + "%")


        query += " ORDER BY time DESC"
        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])

        logging.debug(f"Executing '{query}' query")
        self.cursor.execute(query, params)
        logging.info("querey executed successfully.")

        logging.debug("Fetching data....")
        results = self.cursor.fetchall()

        urls = [{'original_url': row[0], 'shorten_url': row[1], 'time': row[2]} for row in results]
        logging.info(f"Data fetched successfully and converted to dict : {urls}")

        return urls
    