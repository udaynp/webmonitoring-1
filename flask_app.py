from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, make_response,render_template
import requests 
from time import strftime
from flaskext.mysql import MySQL
import os, sys ,shutil
from subprocess import PIPE, Popen
import argparse
from string import Template
import logging
from datetime import datetime
from time import time
import json
import threading
import queue
from threading import Timer

"""
https://buildmedia.readthedocs.org/media/pdf/flask-docs-ja/latest/flask-docs-ja.pdf

"""


username = 'udayradhika'
token = '9ee3129632ccd9bd5b69892a3ccde510e9153a3a'
#token = 'coppergate51'

headers = {'Authorization': 'token ' + token}
repo_name = 'webmonitoring'

app.logger.setLevel(logging.INFO)

app = Flask(__name__)




mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'coppergate51'
app.config['MYSQL_DATABASE_DB'] = 'flask'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app.config['DEBUG'] = True


url_1 = "https://www.intuit.com"
url_2 = "https://en.wikipedia.org/wiki/Intuit"
 # Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
webhook_url_final = 'https://hooks.slack.com/services/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'
responseissue = " Site response crossed threshold"

base_dir_app_log="/Users/upakalapati/Downloads/crafts_demo_logs/"


def sprint(message):
    print ("{0} {1}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),str(message)))



def shell_command(query,IsShell=None):
      #logging.info ("< ------ Running Command ------ >")
      sprint ("< ------ Running Command ------ >")
      #logging.info (query)
      #sprint (query)
      if IsShell:
         run_process = Popen(query, stdout=PIPE, stderr=PIPE, shell=True)
         run_output, run_error = run_process.communicate()
         return run_process.returncode, run_output, run_error


def post_github_issue(title, body=None, labels=["bug"]):
      '''https://developer.github.com/apps/building-oauth-apps/understanding-scopes-for-oauth-apps/'''

      payload = { "title": title,"body": body,"labels": labels}
      login = requests.post('https://api.github.com/'+'repos/'+username+'/'+repo_name+'/issues', auth=(username,token), data=json.dumps(payload))
      sprint(login.json())
      if login.status_code == 201:
        print ('Successfully created Issue {0:s}'.format(title))
      else:
        print ('Could not create Issue {0:s}'.format(title))
        print ('Response:', login.content)


def slack_messages(slack_m):
  response = requests.post(
       webhook_url_final, data=json.dumps(slack_m),
       headers={'Content-Type': 'application/json'}
  )
  if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )


def url_resp(url, q):
    firstevent_url = requests.get(url).elapsed.total_seconds()
    q.put(firstevent_url)


def time_now(test, q):
    last_update_time = strftime("%Y-%m-%d %H:%M:%S")

    sprint("now" + test + str(last_update_time))
    logging.info("time now" + str(last_update_time))

    q.put(last_update_time)


def thread_call_url(url):
    q = queue.Queue()
    threading.Thread(target=url_resp, args=(url, q)).start()
    firstevent_url = q.get()
    sprint(" Url " + url + "  response time is   :" + str(firstevent_url)+"\n")
    logging.info(" Url " + url + "   response time is   :" + str(firstevent_url)+"\n")
    return firstevent_url


def thread_call_time():
    q = queue.Queue()
    threading.Thread(target=time_now, args=("  Time is  :", q)).start()
    last_update_time = q.get()
    sprint(" Time when response time collected " + str(last_update_time)+"\n")
    logging.info(" Time when response time collected " + str(last_update_time)+"\n")
    return last_update_time

def mysql_insert(url, firstevent_url, last_update_time):

    connection = mysql.get_db()
    cursor = connection.cursor()
    #query = "INSERT INTO flask.monitoring (url, time_occured, response_time) VALUES ('https://en.wikipedia.org/wiki/Intuit','2019-04-17 01:27:51','0.777777')"
    query = "INSERT INTO flask.monitoring (url,time_occured,response_time) VALUES ('"+url+"','"+last_update_time+"','"+str(firstevent_url)+"')"
    cursor.execute(query)
    connection.commit()

    sprint(" for Url " + url + "   response time is   :" + str(firstevent_url) + "Mysql insertion is done \n")
    logging.info(" for Url " + url + "   response time is   :" + str(firstevent_url) + "Mysql insertion is done \n")

def threshold_check(url,firstevent_url):
    if firstevent_url > 0.3:

        post_message = "response time is more than threshold please check the web site performance and resources"
        slack_data = {"text": url + "   " + post_message}
        slack_messages(slack_data)

        post_github_issue(title=post_message, body=url + "   " + post_message)

    else:
        sprint(" Url " + url + " response is looks good ")
        logging.info(" Url " + url + " response is looks good ")


def flask_thread_rend(firstevent_url1,firstevent_url2,last_update_time):

    return render_template(
        'html_format.html',
        time_elapsed = firstevent_url1,
        time_elapsed_1 = firstevent_url2,
        url_1=url_1,
        url_2=url_2,
        last_update_time = last_update_time
        )


@app.route("/", methods=['GET'])
def monitoring_whole():

    logging.info(" response test is loading ")
    firstevent_url1 = thread_call_url(url_1)
    firstevent_url2 = thread_call_url(url_2)
    last_update_time = thread_call_time()
    mysql_insert(url_1, firstevent_url1, last_update_time)
    mysql_insert(url_2, firstevent_url2, last_update_time)
    threshold_check(url_1, firstevent_url1)
    threshold_check(url_2, firstevent_url2)
    #flask_thread_rend(firstevent_url1,firstevent_url2,last_update_time)

    return render_template(
        'html_format.html',
        time_elapsed = firstevent_url1,
        time_elapsed_1 = firstevent_url2,
        url_1=url_1,
        url_2=url_2,
        last_update_time = last_update_time
        )


if __name__ == '__main__':
    log_dir = os.path.join(base_dir_app_log, "logs/webmonitoring")
    logfile = os.path.join(log_dir,"Webmonitoring_flask" + datetime.now().strftime('_monitoring_log_%Y_%m_%d_%I_%M_%S.log'))
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename=logfile, level=logging.INFO)
    sprint('-------------------------------- START ---------------------------------')
    logging.info('< --------- START ---------------------- >')

    app.run(debug=True)
