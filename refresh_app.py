import os
import sys
import requests

res = requests.get('http://127.0.0.1:5000')
try:
    res.raise_for_status()
    print(res)
    print(res.status_code)
except Exception as exc:
    exit(1)
    print('There was a problem: %s' % (exc))

