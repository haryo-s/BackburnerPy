import sys
import os
import logging
from flask import Flask

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'BackburnerPy'))

from Monitor import Monitor

# This is an example web service using Flask and BackburnerPy
# Launch this file with the Manager's IP Address as a string and TCP port
# For example: `python flask_server.py "127.0.0.1" 3234`
#
# When visiting the web service, you'll find a brief look at the Manager, the connected servers and current jobs.
try:
    MANAGER_IP = str(sys.argv[1])
    MANAGER_PORT = int(sys.argv[2])
except:
    print("Incorrect arguments.")
    

manager = Monitor(MANAGER_IP, MANAGER_PORT, logging.INFO)

HEAD = """
<head>
    <style>
        h1 {
            display: block;
            font-size: 2em;
            margin-top: 0.67em;
            margin-bottom: 0.67em;
            margin-left: 0;
            margin-right: 0;
            font-weight: bold;
        }

        h2 {
            display: block;
            font-size: 1.5em;
            margin-top: 0.83em;
            margin-bottom: 0.83em;
            margin-left: 0;
            margin-right: 0;
            font-weight: bold;
        }
    </style>
</head>
"""

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    manager.open_connection()

    manager_info = manager.get_manager_info()
    manager_html = "<p class=\"\">\n"
    manager_html += "<p class=\"\">\n<h1>\n" + "Manager: " + str(manager_info.system_info.computer_name) + "</h1>\n</p>\n"
    manager_html += "<p class=\"\">\n<h2>\n" + "User: " + str(manager_info.system_info.user) + "</h2>\n</p>\n"
    manager_html += "<p class=\"\">\n<h2>\n" + "Platform: " + str(manager_info.system_info.platform) + "</h2>\n</p>\n"
    manager_html += "</p>\n"

    server_list = manager.get_server_list()
    server_html_list = "<p class=\"\">\n<h2>\n" + "Servers:" + "</h2>\n</p>\n"
    server_html_list += "<ul class=\"\" style=\"\">\n"
    for item in server_list:
        server_html_list += f"<li class=\"\"> {item.name} </li>\n"
    server_html_list += "</ul>\n"
    
    job_list = manager.get_job_list()
    jobs = []
    for job in job_list:
        jobs.append(manager.get_job(str(job.handle)))

    job_html_list = "<h2>\n" + "Jobs:" + "</h2>\n"
    job_html_list += "<ul class=\"\" style=\"\">\n"
    for job in jobs:
        job_html_list += f"<li class=\"\"> {job.job_info.name}: {job.job_info.tasks_completed}/{job.job_info.number_tasks}</li>\n"
    job_html_list += "</ul>\n"

    html = HEAD + manager_html + server_html_list + job_html_list
    manager.close_connection()

    return html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
