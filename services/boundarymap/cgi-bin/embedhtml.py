#!/usr/bin/python3

import cgi
import cgitb
import urllib.request
import google.oauth2.credentials
import google_auth_oauthlib.flow
import flask
from flask import request

with open('/opt/bitnami/apache2/htdocs/private_ms.html', 'r') as file:
    private_msHTML = file.read()
