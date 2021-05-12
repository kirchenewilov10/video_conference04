import json
from datetime import datetime

def print_log(request, function_name, error_message):
    log_file = open("log.txt", "a")
    log_file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.000Z") + " " + request.body.decode() + " " + function_name + " " + error_message + "\n")
    log_file.close()