cd /Users/upakalapati/Documents/GitHub/webmonitoring
FLASK_APP=flask_app.py flask run  > /tmp/main_flask_app.out 2>&1 &

while :; do
  python refresh_app.py
  sleep 5
  if [ $? -ne 0 ]; then
    echo "site is not running -- app"
    break
  fi
  sleep 5
done
