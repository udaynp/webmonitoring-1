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

url_1 = "https://www.intuit.com"
url_2 = "https://en.wikipedia.org/wiki/Intuit"

base_dir_app_log = "/Users/upakalapati/Downloads/crafts_demo_logs/"


def sprint(message):
    print ("{0} {1}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(message)))


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
    sprint(" Url " + url + " response time is " + str(firstevent_url))
    logging.info(" Url " + url + " response time is " + str(firstevent_url))
    return firstevent_url


def thread_call_time():
    q = queue.Queue()
    threading.Thread(target=time_now, args=("Time is", q)).start()
    last_update_time = q.get()
    sprint(" Time when response time collected " + str(last_update_time))
    logging.info(" Time when response time collected " + str(last_update_time))
    return last_update_time


def monitoring_whole():
    firstevent_url1 = thread_call_url(url_1)
    firstevent_url2 = thread_call_url(url_2)
    last_update_time = thread_call_time()


if __name__ == '__main__':
    log_dir = os.path.join(base_dir_app_log, "logs/webmonitoring")
    logfile = os.path.join(log_dir,
                           "Webmonitoring_flask" + datetime.now().strftime('_monitoring_log_%Y_%m_%d_%I_%M_%S.log'))
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=logfile, level=logging.INFO)
    sprint('-------------------------------- START ---------------------------------')
    logging.info('< --------- START ---------------------- >')
    monitoring_whole()


