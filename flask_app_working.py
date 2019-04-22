from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, make_response,render_template
import requests 
from time import strftime
from flaskext.mysql import MySQL

"""
CREATE TABLE `flask`.`monitoring` (
  `url` VARCHAR(45) NOT NULL,
  `time_occured` TIMESTAMP NULL,
  `response_time` float NULL)
  
  
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


@app.route("/", methods=['GET'])
def monitoring_whole():
    firstevent_url1=str(requests.get(url_1).elapsed.total_seconds())
    firstevent_url2=str(requests.get(url_2).elapsed.total_seconds())
    last_update_time = strftime("%Y-%m-%d %H:%M:%S")
    connection = mysql.get_db()
    cursor = connection.cursor()
    #query = "INSERT INTO flask.monitoring (url, time_occured, response_time) VALUES ('https://en.wikipedia.org/wiki/Intuit','2019-04-17 01:27:51','0.777777')"
    query = "INSERT INTO flask.monitoring (url,time_occured,response_time) VALUES ('"+url_1+"','"+last_update_time+"','"+firstevent_url1+"')"
    cursor.execute(query)
    query = "INSERT INTO flask.monitoring (url,time_occured,response_time) VALUES ('"+url_2+"','"+last_update_time+"','"+firstevent_url2+"')"
    cursor.execute(query)
    #query = "INSERT INTO monitoring (url, time_occured, response_time) VALUES ({0},{1},{2})".format(url_2,last_update_time,firstevent_url2)
    #cursor.execute(query)
    connection.commit()
   
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
