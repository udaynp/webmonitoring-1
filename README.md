# webmonitoring

This is the APP using Flask and Python to monitor the response time of sites.

Same time Whenever there is a incident more than Threshold response time we sent a slack message.

We have integrated with Git issue API , When ever you get response more than Threshold we sent a issue to Git .

We have everything handled with Python.


https://networklore.com/start-task-with-flask/




nohup sh crafts_demo_site.sh > /tmp/crafts_demo_site.out 2>&1 &

tail -f /tmp/main_flask_app.out


FLASK_APP=monitoring_application.py flask run --host 127.0.0.1 --port 8089
