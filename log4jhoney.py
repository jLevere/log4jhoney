from flask import Flask, request
from flask.helpers import make_response
import requests
import json
import re

app = Flask(__name__)

discord_webhook = ""
username = "log4shell bot"

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

login_form = """<!DOCTYPE html>
<head>
<meta charset="utf-8">
<title>Log in to enable Views</title></head>
<!--
        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
              This file is generated from xml source: DO NOT EDIT
        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-->
<body>
<h1>Login to enable Views</h1>
<form method='post' action='/'>
  <b>Username:</b> <input name='username' type='text'/><br/>
  <b>Password:</b> <input name='password' type='password'/><br/>
  <input type='submit' name='submit'/>
</form>
</body></html>
<footer>
<p class="apache">Copyright 2021 The Apache Software Foundation.
<br/>Licensed under the <a href="http://www.apache.org/licenses/LICENSE-2.0">
Apache License, Version 2.0</a>.</p>
</footer>
"""

login_fail = """
<html><head><title>Login Failed</title></head>
<body
><h1>Login Failed</h1>
<br/><a href='/'>
Try again</a>
</body></html>"""

error_page = """
<html><head><title>Please return to index</title></head>
<body
><h1>File Not Found</h1>
<br/><a href='/'>
Try again</a>
</body></html>
"""

def get_req_contents(req):
    content = dict((req.headers).to_wsgi_list())
    if req.form:
        content['form'] = str(json.dumps(req.form))

    if req.args:
        content['args'] = str(json.dumps(req.args))

    return json.dumps(content, indent=4)


def send_hook(req):
    content = get_req_contents(req)

    msg = {
        'username' : username,
        'content' : content
    }

    r = requests.post(discord_webhook, json=msg)
    print(r.text)



@app.route("/", methods=HTTP_METHODS)
def index():
    contents = get_req_contents(request)

    if re.search(r'\$\{jndi:(ldap[s]?|rmi|dns):\/[^\n]+', contents):
        send_hook(request)

    if request.method == 'POST':
        return make_response(login_fail, 200)
    else:
        return make_response(login_form, 200)


@app.errorhandler(Exception)
def handle_error(e):
    return make_response(error_page, 200)

if __name__ == '__main__':
    app.run()