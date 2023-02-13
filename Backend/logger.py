import logging

# warpper function 
def log_action(func):
    def wrapper(*args, **kwargs):
        logging.basicConfig(filename='actions.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        result = func(*args, **kwargs)
        return result
    return wrapper