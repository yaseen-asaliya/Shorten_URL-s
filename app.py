from flask import Flask, request, jsonify, redirect, g
import logging
import Backend.database_configaration as dbc
from Backend.logger import log_action

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = dbc.DatabaseConfigraton()

@log_action
@app.route("/shorten_url", methods=["POST"])
def get_shorten_url():
    original_url = request.json["url"]
    shortened_url = g.db.insert_url(original_url)
    return jsonify({"shortened_url": shortened_url})

@log_action
@app.route('/original_url', methods=['GET'])
def get_full_url():
    short_url = request.json["url"]
    result = g.db.get_full_url(short_url)
    if result:
        original_url = result[0]
        return redirect(original_url)
    else:
        return jsonify({'error': 'Short URL not found'}), 404

@log_action
@app.route('/urls', methods=['GET'])
def get_all_urls():
    date = request.args.get('date')
    search = request.args.get('search')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)
    urls = g.db.get_all_urls(date, search, page, per_page)
    return jsonify({'urls': urls})

if __name__ == "__main__":
    app.run()
