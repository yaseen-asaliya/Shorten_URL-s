from flask import Flask, request, jsonify, redirect, g
import logging
import Backend.database_configaration as dbc
from Backend.logger import log_action

app = Flask(__name__)

@app.before_request
def before_request():
    try:
        logging.debug("Connecting to database...")
        g.db = dbc.DatabaseConfigraton()
        logging.info("Database connected.")
    except Exception as err:
        logging.error(f"Error while connnecting to the database : {err}")
    
@log_action
@app.route("/shorten_url", methods=["POST"])
def get_shorten_url():
   try:
       original_url = request.json["url"]
       logging.info(f"Getting short url for : {original_url}")
       shortened_url = g.db.insert_url(original_url)
       logging.info(f"shoret url is : {shortened_url}")
       return jsonify({"shortened_url": shortened_url})
   except Exception as err:
       logging.error(f"error while getting shore url : {err}") 

@log_action
@app.route('/original_url', methods=['GET'])
def get_original_url():
    try:
        short_url = request.json["url"]
        logging.info(f"Getting original url for : {short_url}")
        result = g.db.get_full_url(short_url)
        logging.info(f"Original url is : {result[0]}")
        if result:
            original_url = result[0]
            return redirect(original_url)
        else:
            return jsonify({'error': 'Short URL not found'}), 404
    except Exception as err:
        logging.error(f"error while get original url : {err}")

@log_action
@app.route('/urls', methods=['GET'])
def get_all_urls():
    try:
        date = request.args.get('date')
        search = request.args.get('search')
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=3, type=int)
        logging.debug(f"Getting based on :- date: {date}, search: {search}, page: {page}, per_page: {per_page}")
        urls = g.db.get_all_urls(date, search, page, per_page)
        logging.info("Got the data successfully.")
        return jsonify({'urls': urls})
    except Exception as err:
        logging.error(f"error while get all url's : {err}")

if __name__ == "__main__":
    app.run()
