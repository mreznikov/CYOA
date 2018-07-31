#encoding=UTF-8
import re

def PrintEnemiesSQL(file):

    text = file.read()

    enemies = re.findall(r'[А-Я].*[А-Я]\b\s\n\n\n.*\n.*', text)

    enemy_dct={}
    id=0
    for enemy in enemies:

        match = re.findall(r'[А-Я].*[А-Я]', enemy)
        name=match[0]

        match=re.findall(r'\d\d?', enemy)
        stamina=match[0]
        mastery=match[1]

        sql='INSERT INTO ENEMIES VALUES('+str(id)+',"'+name+'",'+stamina+','+mastery+',0);'

        print(sql)

        id = id + 1

    file.close()

file = open(r'C:\\Users\\mika\\PycharmProjects\\CYOA\\podzemelye_chernogo_zamka_source.txt', 'r',encoding='UTF-8')
PrintEnemiesSQL(file)