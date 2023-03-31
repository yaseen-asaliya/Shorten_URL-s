import random
import string
import logging
from Backend.logger import log_action

@log_action
def get_shorten_url(original_url):
    logging.info("Getting shorten url...")
    # This if is for test if the URL is already short
    if len(original_url.split("/")) <= 4 and original_url.split("/")[3] == '':
       logging.info(f"{original_url} already short")
       return original_url

    possible_characters = string.ascii_letters + string.digits
    shortened_url = "".join(random.choice(possible_characters) for _ in range(6))
    short_url = "http://shorten.url/" + shortened_url
    logging.info(f"The short url for {original_url} is {short_url}")
    return short_url