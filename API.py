# coding: utf-8
import logging
from flask import Flask, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

#Хранилище данных о сессиях.
sessionStorage = {}



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def Get_Event_by_ID(conn,event_id,session_id,user_id,version,message_id):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    query='SELECT * FROM EVENTS t1 LEFT JOIN ITEMSANDINFO t2 on t1.ID=t2.EVENT_ID LEFT JOIN ENEMIES t3 on t1.ID=t3.EVENT_ID WHERE t1.ID="'+event_id+'"'
    cur.execute(query)

    rows = cur.fetchall()


    buttons = []



    js={}

    for row in rows:
        button = { "title":row[1], "hide": "true"}
        buttons.append(button)

    if len(rows) == 0:
        text = ""
    else:
        text = rows[0][4]

    js={ "response": {
    "text":text,
    "tts": text,
    "buttons": buttons,
    "end_session": "false"
    },
     "session": {
    "session_id": session_id,
    "message_id":  message_id,
    "user_id": user_id
     },
     "version": version
    }
   # print(js)
    return js







#def main():
    #
    # logging.info('Request: %r', request.json)
    #
    # response = {
    #     "version": request.json['version'],
    #     "session": request.json['session'],
    #     "response": {
    #         "end_session": False
    #     },
    #     "request": {
    #         "command": request.json['command'],
    #         "original_utterance": request.json['original_utterance'],
    #         "type": request.json['type'],
    #         "markup": {
    #             "dangerous_context": true
    #         },
    #
    #     }
    #
    #
    # #database = "\\CYOA.db"
    #
    # # create a database connection
    # conn = create_connection(database)
    # event_id=request.json['command']
    # with conn:
    #    js=Get_Event_by_ID(conn,event_id,request.json['session']['session_id'],request.json['session']['user'],request.json['version'])
    #
    # print(js)

# if __name__ == '__main__':
#     main()