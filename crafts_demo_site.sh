cd /Users/upakalapati/Documents/GitHub/webmonitoring
FLASK_APP=flask_app.py flask run  > /tmp/main_flask_app.out 2>&1 &

FLASK_APP=Monitoring_application.py flask run --host 127.0.0.1 --port 8089  > /tmp/main_flask_app_monitoring.out 2>&1 &



while :; do
  sleep 10
  python refresh_app.py
  sleep 10
  if [ $? -ne 0 ]; then
    echo "site is not running -- app"
    break
  fi
  sleep 10
done

