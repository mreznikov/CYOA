#encoding=UTF-8
import re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

#soup = BeautifulSoup(markup, 'xml')

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

#file = open(r'C:\\Users\\miloslav\\PycharmProjects\CYOA\\podzemelye_chernogo_zamka_source.txt', 'r',encoding='UTF-8')
#PrintEnemiesSQL(file)

tree = ET.parse(r'C:\\Users\\miloslav\\PycharmProjects\CYOA\\gamebook.xml')
book = tree.getroot()
events = {}
item_lst = []
item_dct = {}
events_lst=[]
for page in book:
    #print(page.tag)
    #print(page.tag)
    option_lst = []

    for item in page:
        # Получаем список монстров
        #print(item.tag)
        if re.match(r'enemy',item.tag):
            for battle_item in item:
                if re.match(r'enemy.',battle_item.tag):
                    event_id = page.tag[5:]
                    value = battle_item.get('value')
                    value_lst = value.split(';')
                    name = value_lst[0]
                    agility = value_lst[1]
                    mastery = value_lst[2]
                    loyalty = ''
                    damage = ''
                    # if len(value_lst) == 4:
                    #     value_lst2 = value_lst[3].split(':')
                    #     if value_lst2[0] == "loyalty":
                    #         loyalty = value_lst2[1
                    #     elif value_lst2[0] == "damage":
                    #         damage = value_lst2[1]
                    #     elif value_lst2[0] == "damage":
                    #
                    # if len(value_lst) == 5:
                    #     value_lst2 = value_lst[3].split(':')
                    #     loyalty = value_lst2[1]
                    #     value_lst2 = value[4].split(':')
                    #     damage = value_lst2[1]
                    sql = 'INSERT INTO ENEMIES VALUES("'+event_id+'","'+name+'","'+agility+'","'+mastery+'","'+loyalty+'","'+damage+'");'
                    #print(sql)

   # Ищем опции
    for item in page:
        name = page.tag[5:]
        option = ""
        options = {}
        description=""
        spell = ""
        option_item=""
        if re.match(r'jump',item.tag):

            if re.match(r'jump.x.',item.tag):
                option_item = item.get('value')
            else:
                option=re.findall(r'\d+',item.tag)[0]

            if item.tag[-5:] == 'spell':
                spell=item.get('value')

            if item.tag[-4:] == 'info':
                option_item = item.get('value')

            for item2 in page:
                if re.match(r'text', item2.tag):
                    description = item2.get('value')

            event_dct = {'id': name, 'option': option, 'spell': spell, 'option.item': option_item, 'description':description}
            events_lst.append(event_dct)

    #print(events_lst)


    for item in page:
        # Ищем items&info
        if re.match(r'item', item.tag) or re.match(r'info', item.tag):
            item_dct={'ID':page.tag[5:],'ITEM_NAME':item.get('value')}
            item_lst.append(item_dct)
            data = item.get('value').split(';')
            #print('INSERT INTO ITEMSANDINFO VALUES("'+page.tag[5:]+'","'+data[0]+'","'+data[1]+'");')

    #print(option_lst,item_lst)
    #print(description)

for d in events_lst:
    #print(d['id'])
    #print(d['option'])
    #print(d['spell'])
   # print(d['option.item'])
   # print(d['description'])

    print('INSERT INTO EVENTS VALUES("'+d['id']+'","'+d['option']+'","'+d['spell']+'","'+d['option.item']+'","'+d['description']+'");')
