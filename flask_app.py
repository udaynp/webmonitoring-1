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

"""
https://qbox.io/blog/migrating-mysql-data-into-elasticsearch-using-logstash
curl -XPOST 'http://localhost:9200/site-monitoring/_search?pretty=true' -d '{}' -H 'Content-Type: application/json'
curl -XGET "http://localhost:9200/site-monitoring/_search"
https://api.slack.com/apps/AJ037EAJU/incoming-webhooks?success=1
curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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
curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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

"""

"""
CREATE TABLE `flask`.`monitoring` (
  `url` VARCHAR(45) NOT NULL,
  `time_occured` TIMESTAMP NULL,
  `response_time` float NULL)
  
https://logz.io/blog/elk-mac/ 
"""

"""
time to create the request object
Send request
Receive response
Other ways to measure a single request load time is to use urllib:

nf = urllib.urlopen(url)
start = time.time()
page = nf.read()
end = time.time()
nf.close()
"""

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = 'udayradhika'
PASSWORD = 'd9a5eee4961340145d256c011e2a311185980c9d'

# The repository to add this issue to
REPO_OWNER = 'udayradhika'
REPO_NAME = 'webmonitoring'

username = 'udayradhika'
token = 'd9a5eee4961340145d256c011e2a311185980c9d'







app = Flask(__name__)

mysql = MySQL()

 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'coppergate51'
app.config['MYSQL_DATABASE_DB'] = 'flask'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.config['DEBUG'] = True

url = ["https://www.google.com"]

refresh_interval = 60.0

site_down = 'UNREACHABLE'

url_1 = "https://www.intuit.com"

url_2 = "https://en.wikipedia.org/wiki/Intuit"

responseissue = " Site response crossed threshold"

def shell_command(query,IsShell=None):
      #logging.info ("< ------ Running Command ------ >")
      print ("< ------ Running Command ------ >")
      #logging.info (query)
      #sprint (query)
      if IsShell:
         run_process = Popen(query, stdout=PIPE, stderr=PIPE, shell=True)
         run_output, run_error = run_process.communicate()
         return run_process.returncode, run_output, run_error
         
         
 # Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
webhook_url_final = 'https://hooks.slack.com/services/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'


def make_github_issue(title, body=None, labels=None):
    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    headers = {'Authorization': 'token ' + token}

    login = requests.get('https://api.github.com/user', headers=headers)
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    # Create our issue
    issue = {'title': title,
             'body': body,
             'labels': labels}
    # Add the issue to our repository
    r = session.post(login, json.dumps(issue))
    if r.status_code == 201:
        print ('Successfully created Issue {0:s}'.format(title))
    else:
        print ('Could not create Issue {0:s}'.format(title))
        print ('Response:', r.content)

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


@app.route("/", methods=['GET'])
def monitoring_whole():
    firstevent_url1=requests.get(url_1).elapsed.total_seconds()
    firstevent_url2=requests.get(url_2).elapsed.total_seconds()
    last_update_time = strftime("%Y-%m-%d %H:%M:%S")
    connection = mysql.get_db()
    cursor = connection.cursor()
    #query = "INSERT INTO flask.monitoring (url, time_occured, response_time) VALUES ('https://en.wikipedia.org/wiki/Intuit','2019-04-17 01:27:51','0.777777')"
    query = "INSERT INTO flask.monitoring (url,time_occured,response_time) VALUES ('"+url_1+"','"+last_update_time+"','"+str(firstevent_url1)+"')"
    cursor.execute(query)
    query = "INSERT INTO flask.monitoring (url,time_occured,response_time) VALUES ('"+url_2+"','"+last_update_time+"','"+str(firstevent_url2)+"')"
    cursor.execute(query)
    #query = "INSERT INTO monitoring (url, time_occured, response_time) VALUES ({0},{1},{2})".format(url_2,last_update_time,firstevent_url2)
    #cursor.execute(query)
    connection.commit()
    
    if firstevent_url1 > 0.1:
         
         slack_data={"text":"https://www.intuit.com, response time is more than threshold please check the web site performance and resources"}
         slack_messages(slack_data)
         
         make_github_issue(url1, slack_data, responseissue)

    else  :
       print("all looks good ") 
    
    if   firstevent_url2 > 0.1 :              
         slack_data={"text":"https://en.wikipedia.org/wiki/Intuit, response time is more than  threshold  please check the web site performance and resources"}
         slack_messages(slack_data)
         make_github_issue(url2, slack_data, responseissue)
 
    else  :
       print("all looks good ")
       
       
    return render_template(
        'html_format.html',
        time_elapsed = firstevent_url1,
        time_elapsed_1 = firstevent_url2,
        url_1=url_1,
        url_2=url_2,
        last_update_time = last_update_time              
        )

if __name__ == '__main__':
    print("******Start*****")
    app.run()
