import sqlite3
import logging
import datetime
import Backend.short_url_modules as sh
from Backend.logger import log_action

class DatabaseConfigraton:
    @log_action
    def __init__(self):
        try:
            self.short = sh.ShortUrl()
            logging.debug("Connecting to the database.")
            self.connection = sqlite3.connect('shorten_urls_app.db')
            self.cursor = self.connection.cursor()
            logging.info("Database connected successfully.")
            self.create_table_in_db()
        except sqlite3.Error as err:
            logging.error(f"An error occurred while connecting to the database: {err}")
    
    @log_action
    def create_table_in_db(self):
        try:
            logging.debug("Creating tables in database...")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS url (time TIMESTAMP, original_url TEXT, shorten_url TEXT);")
            logging.info("Table URL created successfully.")
            self.connection.commit()
        except sqlite3.InternalError as err:
            logging.error(f"Error setting up database tables: {err}")
        
    @log_action
    def insert_url(self, original_url):
        try:
            if not self.check_original_url_if_exsist(original_url):
                logging.debug(f"Genarating short url for {original_url}")
                short_url = self.short.get_shorten_url(original_url)
                
                logging.debug("Inserting URL's into url table...")
                self.cursor.execute("INSERT INTO url (time, original_url, shorten_url) VALUES (?,?,?)",
                                    (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), original_url, short_url))
                self.connection.commit()
                logging.info("Inserting done successfully.")
                return short_url
            else:
                short_url = self.get_shorten_url(original_url)[0]
                logging.warning(f"{original_url} already has shorten url : {short_url} stored in the database")
                return short_url
            
        except sqlite3.InternalError as err:
            logging.error(f"Error while inserting data in table: {err}")
    
    @log_action
    def get_full_url(self, short_url):
        self.cursor.execute("SELECT original_url FROM url WHERE shorten_url=?", (short_url,))
        logging.debug("Selecting original_url from database...")
        return self.cursor.fetchone()
         
    @log_action
    def get_shorten_url(self, original_url):
        self.cursor.execute("SELECT shorten_url FROM url WHERE original_url=?", (original_url,))
        logging.debug("Selecting shorten_url from database...")
        return self.cursor.fetchone()
        
    @log_action
    def check_original_url_if_exsist(self, original_url):
        logging.info(f"checking if the url {original_url} is exist")
        self.cursor.execute("SELECT original_url FROM url WHERE original_url=?", (original_url,))
        if self.cursor.fetchone():
            return True
        return False
    
    @log_action
    def get_all_urls(self, date, search, page, per_page):
        query = "SELECT time, original_url, shorten_url FROM url"
        params = []
        
        if date and search:
            query += " WHERE time LIKE ? AND original_url LIKE ?"
            params.append(date + "%")
            params.append("%" + search + "%")
        else:
            if date:
               query += " WHERE time LIKE ?"
               params.append(date + "%")
            
            if search:
                query += " WHERE original_url LIKE ?"
                params.append("%" + search + "%")
               
        
        query += " ORDER BY time DESC"
        query += " LIMIT ? OFFSET ?"
        params.extend([per_page, (page - 1) * per_page])
        
        logging.debug(f"Executing '{query}' query")
        self.cursor.execute(query, params)
        logging.info("querey executed successfully.")
        
        logging.debug("Fetching data....")
        results = self.cursor.fetchall()
        
        urls = [{'original_url': row[0], 'shorten_url': row[1], 'time': row[2]} for row in results]
        logging.info(f"Data fetched successfully and converted to dict : {urls}")
        
        return urls
