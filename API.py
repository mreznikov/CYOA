# coding: utf-8
from __future__ import unicode_literals


import logging
from flask import Flask, request

import sqlite3
from sqlite3 import Error

import time
import re

import codecs

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

#Хранилище данных о сессиях.
sessionStorage = {}

def RequestQualityCheck(conn,request):
    command = request.json['request']['command']
    session_id = request.json['session']['session_id']
    user_id=request.json['session']['user_id']
    command_number = None
    response_id = None
    cur = conn.cursor()

    # Проверяем, что команда - это число
    try:
        val = int(command)
        command_number = True
    except ValueError:
        command_number = False

    # Если команда, число - проверяем, что оно меньше, чем max event_id
    if command_number is True:
        query = 'SELECT MAX(ID) FROM (SELECT CAST(ID as int)as ID FROM EVENTS ) '
        cur.execute(query)
        rows = cur.fetchall()
        max_event_id = rows[0][0]
        if val > max_event_id or val < 0:
            response_id="1"
        if command[0] == "0":
          response_id = "2"

    if command_number is False:
        if command != u"Далее" and command != u"далее" and command != "test" and command !="" and command !="Повторить" and command !="повторить":
            response_id="2"
        elif command == u"Повторить" or command == u"повторить":
            response_id="3"



    if response_id is None:
        return None
    else:
        #Получаем текст для Response из BD
        if response_id=="3": # если пользователь просит повторить
            query ='SELECT USER_DECISION FROM USER_LOG WHERE correct_event_id=1 and USER_ID="'+user_id+'" and SESSION_ID="' + session_id +'" ORDER BY ID DESC LIMIT 1'
        else:
            query = 'SELECT DESCRIPTION FROM OPTIONAL_RESPONSES WHERE ID=' + response_id
        cur.execute(query)
        rows = cur.fetchall()
        response = rows[0][0]
        return response




def Get_Request(conn,request):
    try:
        event_id = request.json['request']['command']
        if event_id == "" or event_id == "test":  # Здесь отредактировать для Вступления
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
    description2 = 0

    # Если это первое сообщение в рамках сессии, то проставляем event_id
    if message_id == 1:
        event_id = "1"

    if request.json['request']['command'] == u'далее' or request.json['request']['command'] == u'Далее':
        cur = conn.cursor()
        query = 'SELECT USER_DECISION FROM USER_LOG WHERE SESSION_Id = "' + session_id + '" ORDER BY ID DESC'
        cur.execute(query)
        rows = cur.fetchall()
        event_id = rows[0][0]
        description2 = 1

    if request.json['request']['command'] == u'Повторить' or request.json['request']['command'] == u'повторить':
        cur = conn.cursor()
        query = 'SELECT USER_DECISION FROM(SELECT *, CAST(USER_DECISION as integer) as nottext FROM  USER_LOG WHERE SESSION_Id = "' + session_id + '" and nottext <> 0  ORDER BY ID DESC)'

        cur.execute(query)
        rows = cur.fetchall()
        if cur.rowcount == 1:
            event_id = 1
        else:
            event_id = rows[1][0]
        description2 = 0

    JsonDict =	{
      "event_id": event_id,
      "session_id": session_id,
      "user_id":user_id ,
      "version": "1.0",
      "message_id": message_id ,
      "description2":description2
    }
    return JsonDict

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

def Generate_Response_JSON( ResponseDict,description,options):

    buttons = []

    js = {}

    for option in options:
        button = {"title": option, "hide": True}
        buttons.append(button)


    js = {"response": {
        "text": description,
        "tts": description,
        "buttons": buttons,
        "end_session": "false"
    },
        "session": {
            "session_id": ResponseDict["session_id"],
            "message_id": int(ResponseDict["message_id"]),
            "user_id": ResponseDict["user_id"]
        },
        "version": ResponseDict["version"]
    }

    return js


# print(js)

def Get_Event_by_ID(conn,ResponseDict):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """


    cur = conn.cursor()
    query='SELECT * FROM EVENTS t1 LEFT JOIN ITEMSANDINFO t2 on t1.ID=t2.EVENT_ID LEFT JOIN ENEMIES t3 on t1.ID=t3.EVENT_ID WHERE t1.ID="'+ResponseDict["event_id"]+'"'

    cur.execute(query)

    rows = cur.fetchall()


    options = []

    for row in rows:
        if rows[0][5] != "" and ResponseDict["description2"] == 0:
            options.append("Далее")
            break
        options.append(row[1])
    options.append("Повторить")

    if len(rows) == 0:
        text = ""
    elif ResponseDict["description2"] == 0:
        text = rows[0][4]
    else:
        text = rows[0][5]

    return text,options

def WriteLog(session_id,USER_DECISION,response,connection,USER_ID):
    correct_used_id=""

  #  now = time.strftime("%c")
    ## date and time representation
    #print
    #"Current date & time " + time.strftime("%c")
    dec_datetime = time.strftime("%c")
    if response is None:
        connection.execute('''INSERT INTO USER_LOG (SESSION_ID,USER_DECISION,correct_event_id,USER_ID,dec_datetime) VALUES (?,?,?,?,?)''',
                  (session_id, USER_DECISION, "1", USER_ID, dec_datetime))
    else:
        connection.execute('''INSERT INTO USER_LOG (SESSION_ID,USER_DECISION,correct_event_id,USER_ID,dec_datetime) VALUES (?,?,?,?,?)''',
                  (session_id, USER_DECISION, "0", USER_ID, dec_datetime))

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

def getStringWithDecodedUnicode(value):
    findUnicodeRE = re.compile('\\\\u([\da-f]{4})')

    def getParsedUnicode(x):
        return chr(int(x.group(1), 16))

    return findUnicodeRE.sub(getParsedUnicode, str(value))
