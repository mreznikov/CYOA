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
        #print(sql)
        id = id + 1
    file.close()

#file = open(r'C:\\Users\\miloslav\\PycharmProjects\CYOA\\podzemelye_chernogo_zamka_source.txt', 'r',encoding='UTF-8')
#PrintEnemiesSQL(file)

tree = ET.parse(r'C:\\Users\\miloslav\\PycharmProjects\\CYOA\\gamebook.xml')
book = tree.getroot()
events = {}
item_lst = []
item_dct = {}
events_lst=[]
enemies_lst=[]
II_lst=[]

for page in book:
    name = page.tag[5:]

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
                    enemies_lst.append(sql)



   # Ищем опции
    for item in page:
        name = page.tag[5:]
        option = ""
        options = {}
        description=""
        spell = ""
        option_item = ""
        char_change = ""



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

        if item.tag[-5:] == 'event':
            char_change=item.get('value')

        if (option_item =="" or option =="" or spell == "") == True and (option_item =="" and option =="" and spell == "") == False:
            event_dct = {'id': name, 'option': option, 'spell': spell, 'option.item': option_item,'description': description,'char_change':char_change}
            events_lst.append(event_dct)

        if events_lst[-1]['id'] != name:
            event_dct = {'id': name, 'option': option, 'spell': spell, 'option.item': option_item,'description': description,'char_change':char_change}
            events_lst.append(event_dct)




    #print(events_lst)


    for item in page:
        # Ищем items&info
        if re.match(r'item', item.tag) or re.match(r'info', item.tag):
            item_dct={'ID':page.tag[5:],'ITEM_NAME':item.get('value')}
            item_lst.append(item_dct)
            data = item.get('value').split(';')
            #print('INSERT INTO ITEMSANDINFO VALUES("'+page.tag[5:]+'","'+data[0]+'","'+data[1]+'");')
            text='INSERT INTO ITEMSANDINFO VALUES("'+page.tag[5:]+'","'+data[0]+'","'+data[1]+'");\n'
            II_lst.append(text)


    #print(option_lst,item_lst)
    #print(description)

with open('II.txt', 'w') as f1:
    for ii in II_lst:
        f1.write(ii+'\n')
    f1.close()


with open('ENEMIES.txt', 'w') as f:

    for en in enemies_lst:
        f.write(en+'\n')
    f.close()

with open('EVENTS.txt', 'w') as f:
    for d in events_lst:
        #print(d['id'])
        #print(d['option'])
        #print(d['spell'])
       # print(d['option.item'])
       # print(d['description'])

        if len(d['description'])<=1024:
            text='INSERT INTO EVENTS VALUES("'+d['id']+'","'+d['option']+'","'+d['spell']+'","'+d['option.item']+'","'+d['description']+'","'+''+'","'+d['char_change']+'");'
        else:
            d1 = ""
            d2 = ""
            str=d['description'] # 163
            print(d['id'])
            for c in range(len(str)):
                #print(str[0:1024-c])
                if str[1024-c] == '.':
                    d1=str[0:1024-c]+". Для продолжения, скажите Далее"
                    d2=str[1025-c:]
                    break

            d['description'] = d1
            d['description2'] =d2
            text='INSERT INTO EVENTS VALUES("'+d['id']+'","'+d['option']+'","'+d['spell']+'","'+d['option.item']+'","'+d['description']+'","'+d['description2']+'","'+d['char_change']+'");'


        f.write(text)
        f.write('\n')
    f.close()
