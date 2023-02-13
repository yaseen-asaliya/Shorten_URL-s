import random
import string
import logging
from Backend.logger import log_action

class ShortUrl:    
    # This function is for return the domain name without "www" or ".com"
    @log_action
    def get_domain_name(self, original_url):
        full_domain = original_url.split("/")[2].split(".")
        logging.info(f"Genarating domain name from {original_url}")
        if "www" in full_domain:
            return ".".join(full_domain[1:-1])
        
        return ".".join(full_domain[:-1])

    @log_action
    def get_shorten_url(self, original_url):
        logging.info("Getting shorten url...")
        # This if is for test if the URL is already short
        if len(original_url.split("/")) <= 4 and original_url.split("/")[3] == '':
            logging.info(f"{original_url} already short")
            return original_url
        
        possible_characters = string.ascii_letters + string.digits
        shortened_url = "".join(random.choice(possible_characters) for _ in range(6))
        domain = self.get_domain_name(original_url)
        logging.info(f"Domain name genarated : {domain}")
        short_url = "https://" + domain + "/" + shortened_url
        logging.info(f"The short url for {original_url} is {short_url}")
        return short_url

