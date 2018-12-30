# coding: utf-8
from __future__ import unicode_literals
from API import *
from flask import Flask
from flask import Response
from flask import request
import logging
from logging.handlers import RotatingFileHandler
import json
import re
import sys
import codecs


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
    options = []

    # Получаем JSON Request от Алисы
    logging.info('Request: %r', request.json)

    database = "CYOA.db"
    conn = create_connection(database)
    c = conn.cursor()

    # Забираем значения из JSON Request
    RequestDict = Get_Request(conn,request)

    # Проверяем качество запроса пользователя
    response = RequestQualityCheck(conn,request)
    if request.json['request']['command'] == u"повторить" or request.json['request']['command'] == u"Повторить":
        RequestDict['event_id']=response
        response=None
    # Логируем действия пользователя

    WriteLog(RequestDict["session_id"], RequestDict["event_id"],response,c,RequestDict["user_id"])

    # Получаем текст и опции
    if response is None:
        description, options = Get_Event_by_ID(conn, RequestDict)
    else:
        description = response

    #Формируем и возвращаемся Алисе JSON Respone. Ищем в BD event_id пользователя
    js = Generate_Response_JSON(RequestDict,description,options)
    print(js)
    conn.commit()
    conn.close()

    #jsonString= getStringWithDecodedUnicode(js)

    #return Response(jsonString)
    #return Response(json.dumps(js, ensure_ascii=False, indent=2))#.encode('utf-8'))
    return json.dumps(js, ensure_ascii=False, indent=2).encode('utf-8')



if __name__ == '__main__':

    # initialize the log handler
    logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)

    # set the log handler level
    logHandler.setLevel(logging.INFO)

    # set the app logger level
    app.logger.setLevel(logging.INFO)

    app.logger.addHandler(logHandler)

    app.run()


