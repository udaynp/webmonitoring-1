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
from logging.handlers import RotatingFileHandler
import urllib2
import socket



app = Flask(__name__)
base_dir_app_log="/Users/upakalapati/Downloads/crafts_demo_logs/"
app.logger.setLevel(logging.DEBUG)  # use the native logger of flask
app.logger.disabled = False
handler = logging.handlers.RotatingFileHandler(
    base_dir_app_log+datetime.now().strftime('web_monitoring_log_%Y_%m_%d_%I_%M_%S.log'),
    'a',
    maxBytes=1024 * 1024 * 100,
    backupCount=20
    )

formatter = logging.Formatter(\
    "%(asctime)s - %(levelname)s - %(name)s: \t%(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)
log.addHandler(handler)

"""
https://buildmedia.readthedocs.org/media/pdf/flask-docs-ja/latest/flask-docs-ja.pdf

"""

logging.basicConfig(level=logging.INFO)

username = 'udayradhika'
token = 'f7adca866868c89ff7f4518ba1a58274d939f17e'
#token = 'coppergate51'

headers = {'Authorization': 'token ' + token}
repo_name = 'webmonitoring'





#app.logger.setLevel(logging.INFO)


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
url_3 = "https://www.google.com"
 # Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
#webhook_url_final = 'https://hooks.slack.com/services/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'
#webhook_url_final = 'https://hooks.slack.com/services/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'
webhook_url_final = 'https://hooks.slack.com/services/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'

responseissue = " Site response crossed threshold"




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
      print(login.json())
      if login.status_code == 201:
        print ('Successfully created Issue {0:s}'.format(title))
        app.logger.info ('Successfully created Issue {0:s}'.format(title))
      else:
        print ('Could not create Issue {0:s}'.format(title))
        app.logger.info  ('Could not create Issue {0:s}'.format(title))
        print ('Response:', login.content)
        app.logger.info ('Response:', login.content)


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
    app.logger.info("time now" + str(last_update_time))

    q.put(last_update_time)


def thread_call_url(url):
    q = queue.Queue()
    threading.Thread(target=url_resp, args=(url, q)).start()
    firstevent_url = q.get()
    sprint(" Url " + url + "  response time is   :" + str(firstevent_url)+"\n")
    app.logger.info(" Url " + url + "   response time is   :" + str(firstevent_url)+"\n")
    return firstevent_url


def thread_call_time():
    q = queue.Queue()
    threading.Thread(target=time_now, args=("  Time is  :", q)).start()
    last_update_time = q.get()
    sprint(" Time when response time collected " + str(last_update_time)+"\n")
    app.logger.info(" Time when response time collected " + str(last_update_time)+"\n")
    return last_update_time

def mysql_insert(url, firstevent_url, last_update_time):

    connection = mysql.get_db()
    cursor = connection.cursor()
    #query = "INSERT INTO flask.monitoring (url, time_occured, response_time) VALUES ('https://en.wikipedia.org/wiki/Intuit','2019-04-17 01:27:51','0.777777')"
    query = "INSERT INTO flask.monitoring (url,time_occured,response_time) VALUES ('"+url+"','"+last_update_time+"','"+str(firstevent_url)+"')"
    cursor.execute(query)
    connection.commit()

    sprint(" for Url " + url + "   response time is   :" + str(firstevent_url) + "\nMysql insertion is done \n")
    app.logger.info(" for Url " + url + "   response time is   :" + str(firstevent_url) + "\nMysql insertion is done \n")

def threshold_check(url,firstevent_url,status_app_url):
    if status_app_url == 200:

                if firstevent_url > 0.3:

                    post_message = "response time is more than threshold please check the web site performance and resources"
                    slack_data = {"text": url + "   " + post_message}
                    slack_messages(slack_data)

                    post_github_issue(title=post_message, body=url + "   " + post_message)

                else:
                    sprint(" \nUrl " + url + " response is looks good \n")
                    app.logger.info(" \nUrl " + url + " response is looks good \n")


    else:
                post_message = "{0} is Down Please check the internet and {1}  ".format(url,url)
                slack_data = {"text": url + "   " + post_message}
                slack_messages(slack_data)


def flask_thread_rend(firstevent_url1,firstevent_url2,last_update_time):

    return render_template(
        'html_format.html',
        time_elapsed = firstevent_url1,
        time_elapsed_1 = firstevent_url2,
        url_1=url_1,
        url_2=url_2,
        last_update_time = last_update_time
        )


def status_check_url( url, timeout=5 ):
    try:
        return urllib2.urlopen(url,timeout=timeout).getcode()
    except urllib2.URLError as e:
        return False
    except socket.timeout as e:

        sprint(" \nUrl " + url + " is not running and Main App is down \n")
        app.logger.info(" \nUrl " + url + " is not running and Main App is down  \n")
        return False



@app.route("/", methods=['GET'])
def monitoring_whole():

    app.logger.info (" \n ***************response test is loading *************\n")
    status_app_url_1 = status_check_url(url_1)
    status_app_url_2 = status_check_url(url_2)
    status_app_url_3 = status_check_url(url_3)
    #status_app_url_1 = 200
    #status_app_url_2 = 400
    if status_app_url_1 == 200:
            firstevent_url1 = thread_call_url(url_1)
            last_update_time = thread_call_time()
            mysql_insert(url_1, firstevent_url1, last_update_time)
            threshold_check(url_1, firstevent_url1,status_app_url_1)

    else:

            firstevent_url1 = "99999"
            last_update_time = strftime("%Y-%m-%d %H:%M:%S")
            sprint('There was a problem: with main app ')
            mysql_insert(url_1, firstevent_url1, last_update_time)
            app.logger.info('There was a problem in {0}  please check the Url immidiatley:'.format(url_1))

    if status_app_url_2 == 200:

            firstevent_url2 = thread_call_url(url_2)
            last_update_time = thread_call_time()

            mysql_insert(url_2, firstevent_url2, last_update_time)

            threshold_check(url_2, firstevent_url2,status_app_url_2)

    else:

        firstevent_url2 = "99999"
        last_update_time = strftime("%Y-%m-%d %H:%M:%S")
        sprint('There was a problem: with main app ')
        mysql_insert(url_2, firstevent_url2, last_update_time)
        app.logger.info('There was a problem in {0}  please check the Url immidiatley:'.format(url_2))

    if status_app_url_3 == 200:

            firstevent_url3 = thread_call_url(url_3)
            last_update_time = thread_call_time()

            mysql_insert(url_3, firstevent_url3, last_update_time)

            threshold_check(url_3, firstevent_url3,status_app_url_3)


    else:

        firstevent_url3 = "99999"
        last_update_time = strftime("%Y-%m-%d %H:%M:%S")
        sprint('There was a problem: with main app ')
        mysql_insert(url_3, firstevent_url3, last_update_time)
        app.logger.info('There was a problem in {0}  please check the Url immidiatley:'.format(url_3))

    #flask_thread_rend(firstevent_url1,firstevent_url2,last_update_time)

    return render_template(
        'html_format.html',
        time_elapsed = firstevent_url1,
        time_elapsed_1 = firstevent_url2,
        time_elapsed_2=firstevent_url3,
        url_1=url_1,
        url_2=url_2,
        url_3=url_3,
        last_update_time = last_update_time
        )

if __name__ == '__main__':

    app.logger.info("Logging is set up.")
    app.logger.info("Monitoring of Url {0}  and Url {1} is starting.".format(url_1,url_2))
    app.run()
    



