from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, make_response, render_template
import requests
from time import strftime
from flaskext.mysql import MySQL
import os, sys, shutil
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
base_dir_app_log = "/Users/upakalapati/Downloads/crafts_demo_logs/"
app.logger.setLevel(logging.DEBUG)  # use the native logger of flask
app.logger.disabled = False
handler = logging.handlers.RotatingFileHandler(
    base_dir_app_log + datetime.now().strftime('web_monitoring_log_%Y_%m_%d_%I_%M_%S.log'),
    'a',
    maxBytes=1024 * 1024 * 100,
    backupCount=20
)

formatter = logging.Formatter( \
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
# token = 'coppergate51'

headers = {'Authorization': 'token ' + token}
repo_name = 'webmonitoring'

# app.logger.setLevel(logging.INFO)


mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'coppergate51'
app.config['MYSQL_DATABASE_DB'] = 'flask'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app.config['DEBUG'] = True

url_1 = "http://127.0.0.1:5000"

# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
webhook_url_final = 'https://hooks.slack.com/services/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'
responseissue = " Site response crossed threshold"


def sprint(message):
    print ("{0} {1}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(message)))


def shell_command(query, IsShell=None):
    # logging.info ("< ------ Running Command ------ >")
    sprint("< ------ Running Command ------ >")
    # logging.info (query)
    # sprint (query)
    if IsShell:
        run_process = Popen(query, stdout=PIPE, stderr=PIPE, shell=True)
        run_output, run_error = run_process.communicate()
        return run_process.returncode, run_output, run_error





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
    sprint(" Url " + url + "  response time is   :" + str(firstevent_url) + "\n")
    app.logger.info(" Url " + url + "   response time is   :" + str(firstevent_url) + "\n")
    return firstevent_url


def thread_call_time():
    q = queue.Queue()
    threading.Thread(target=time_now, args=("  Time is  :", q)).start()
    last_update_time = q.get()
    sprint(" Time when response time collected " + str(last_update_time) + "\n")
    app.logger.info(" Time when response time collected " + str(last_update_time) + "\n")
    return last_update_time


def mysql_insert(url, firstevent_url, last_update_time):
    connection = mysql.get_db()
    cursor = connection.cursor()
    query = "INSERT INTO flask.monitoring (url,time_occured,response_time) VALUES ('" + url + "','" + last_update_time + "','" + str(
        firstevent_url) + "')"
    cursor.execute(query)
    connection.commit()

    sprint(" for Url " + url + "   response time is   :" + str(firstevent_url) + "\nMysql insertion is done \n")
    app.logger.info(
        " for Url " + url + "   response time is   :" + str(firstevent_url) + "\nMysql insertion is done \n")


def threshold_check(url, firstevent_url):
    if firstevent_url > 0.3:

        post_message = "response time is more than threshold please check the web site performance and resources"
        slack_data = {"text": url + "   " + post_message}
        slack_messages(slack_data)


    else:
        sprint(" \nUrl " + url + " response is looks good \n")
        app.logger.info(" \nUrl " + url + " response is looks good \n")


def flask_thread_rend(firstevent_url1, firstevent_url2, last_update_time):
    return render_template(
        'html_format.html',
        time_elapsed=firstevent_url1,
        time_elapsed_1=firstevent_url2,
        url_1=url_1,
        last_update_time=last_update_time
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
    status_app_url=status_check_url(url_1)


    try:

            if status_app_url == 200:
                firstevent_url1 = thread_call_url(url_1)
                last_update_time = thread_call_time()
                mysql_insert(url_1, firstevent_url1, last_update_time)
                threshold_check(url_1, firstevent_url1)

                    # flask_thread_rend(firstevent_url1,firstevent_url2,last_update_time)


            else:
                firstevent_url1 = "99999"
                last_update_time = strftime("%Y-%m-%d %H:%M:%S")
                sprint('There was a problem: with main app ')
                status_app = "Down"
                mysql_insert(url_1, firstevent_url1, last_update_time)
                threshold_check(url_1, firstevent_url1)
                app.logger.info('There was a problem in Main APP please check the APP immidiatley:')





            app.logger.info("status_app_url is {0}.".format(status_app_url))

            app.logger.info("response time is for firstevent_url1 is {0}.".format(firstevent_url1))
            return render_template(
                'app_monitoring.html',
                time_elapsed=firstevent_url1,
                status_app=status_app_url,
                url_1=url_1,
                last_update_time=last_update_time

               )

    except Exception as exc:
        sprint('There was a problem: %s' % (exc))
        app.logger.info('There was a problem in Main APP please check the APP immidiatley: %s' % (exc))


if __name__ == '__main__':
    app.logger.info("Logging is set up.")
    app.logger.info("Monitoring is starting.")

    app.run()




