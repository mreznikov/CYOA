# coding: utf-8
from API import create_connection, Get_Event_by_ID
from flask import Flask
from flask import Response
from flask import request
import logging
from logging.handlers import RotatingFileHandler
import json
from flask import jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

#Хранилище данных о сессиях.
sessionStorage = {}

@app.route("/log")
def logTest():
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')
    return "Code Handbook !! Log testing."

@app.route('/', methods=['POST'])

def main():

    logging.info('Request: %r', request.json)

    #event_id = request.args.get('id', default=1, type=str)
    database = "CYOA.db"
    conn = create_connection(database)

    try:
        event_id = request.json['request']['command']
        if event_id == "" or event_id == "test":
            event_id = "1"
    except:
        event_id = "1"
    try:
        session_id = request.json['session']['session_id']
    except:
        session_id = "0"
    try:
        user_id = request.json['session']['user_id']
    except:
        user_id = "0"
    try:
        message_id = request.json['session']['message_id']
    except:
        message_id = 1

    #print(event_id)

    if message_id==1:
        event_id="1"

    #print(conn, event_id, session_id, user_id, "1.0",message_id)
    with conn:
        js = Get_Event_by_ID(conn, event_id, session_id, user_id, "1.0",message_id)

    return Response(json.dumps(js,ensure_ascii=False).encode('utf8'))

if __name__ == '__main__':

    # initialize the log handler
    logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)

    # set the log handler level
    logHandler.setLevel(logging.INFO)

    # set the app logger level
    app.logger.setLevel(logging.INFO)

    app.logger.addHandler(logHandler)

    app.run()