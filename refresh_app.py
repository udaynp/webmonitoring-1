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


"""
import os
import sys
import requests
import pickle, os, sys, logging
from httplib import HTTPConnection, socket
from smtplib import SMTP

url="http://127.0.0.1:5000"


def get_response(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        print(res)
        print(res.status_code)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except socket.error:
        print(socket.error)
        return None
        exit(1)
    except Exception as exc:
        print('There was a problem: %s' % (exc))


status_report=get_response(url)
print(status_report)

# working


import urllib2
import socket

def check_url( url, timeout=5 ):
    try:
        return urllib2.urlopen(url,timeout=timeout).getcode()
    except urllib2.URLError as e:
        return False
    except socket.timeout as e:
        print False

url="http://127.0.0.1:5000"
print check_url(url)  #True
status=check_url(url)
print(status)
            
"""
