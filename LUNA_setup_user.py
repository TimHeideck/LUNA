#!/usr/bin/env python3
from distutils.dir_util import copy_tree
import time
import json
import sys
import os
from LUNA_setup_wrapper import *

def end_config(config_data, system_name):
    if not os.path.exists('server/users/' + config_data['User_Info']['name']):
        os.mkdir('server/users/' + config_data['User_Info']['name'])
    try:
        copy_tree('server/resources/user_default', 'server/users/' + config_data['User_Info']['name'])
    except:
        print('\n' + color.RED + '[ERROR]' + color.END + ' Fehler beim kopieren der Dateien. Bitte versuche, den Setup-Assistent mit Root-Rechten auszuführen.')
        sys.exit()
    print('\nDie Konfiguration dieses {}-Nutzerkontos ist abgeschlossen. Sobald du diesen Assistenten beendest, '
          'werden sämtliche Daten im Ordner "server/users/{}" gespeichert.\n'
          'Dort kannst du sie jederzeit bearbeiten, für eine andere {}-Installation kopieren oder persönliche Module für den Nutzer hinzufügen.\n'
          'Als nächstes kannst du einen weiteren Nutzer einrichten '
          'oder mit dem entsprechenden Assistenten Räume hinzufügen, sofern nicht bereits geschehen.'.format(system_name,config_data['User_Info']['name'],system_name))
    with open('server/LUNA_config.json', 'r') as server_config_file:
        server_config_data = json.load(server_config_file)
    if server_config_data['use_facerec']:
        time.sleep(1)
        print('\nUm die Gesichtserkennung für diesen Nutzer zu trainieren, solltest du außerdem einige Fotos von diesem Nutzer im Ordner '
              '"server/users/{}/pictures" ablegen und nach dem Start deines {}-Systems mit dem Kommando "Trainiere die Gesichtserkennung neu"'
              ' das Training einleiten.'.format(config_data['User_Info']['name'], system_name))
    enterFinalize()
    print('\nDie neuen Daten werden gespeichert...')
    with open('server/users/' + config_data['User_Info']['name'] + '/User_Info.json', 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print('\n[{}] Auf wiedersehen!\n'.format(system_name.upper()))
    sys.exit()

########################### ANFANG ###########################
try:
    os.remove('server/users/README.txt')
except FileNotFoundError:
    pass

if not os.path.exists('server/resources/user_default/User_Info.json'):
    print('\n' + color.RED + '[ERROR]' + color.END + ' Die nötigen Dateien (Ordner "server/resources/user_default") für diesen Setup-Schritt konnten nicht gefunden werden.\n'
          'Hast du die Dateien heruntergeladen?\n'
          'Befindet sich das Setup-Skript im richtigen Ordner?')
    enterFinalize()
    sys.exit()

if not os.path.exists('server/users'):
    print('\n' + color.RED + '[ERROR]' + color.END + ' Die nötigen Dateien (Ordner "server/users") für diesen Setup-Schritt konnten nicht gefunden werden.\n'
          'Hast du die Dateien heruntergeladen?\n'
          'Befindet sich das Setup-Skript im richtigen Ordner?')
    enterFinalize()
    sys.exit()

if not os.path.exists('server/LUNA_config.json'):
    print('\n' + color.RED + '[ERROR]' + color.END + ' Die nötigen Dateien ("server/LUNA_config.json") für diesen Setup-Schritt konnten nicht gefunden werden.\n'
          'Hast du die Dateien heruntergeladen?\n'
          'Befindet sich das Setup-Skript im richtigen Ordner?')
    enterFinalize()
    sys.exit()

with open('server/LUNA_config.json', 'r') as server_config_file:
    server_config_data = json.load(server_config_file)
system_name = server_config_data['System_name']

print('Willkommen zum Setup-Assistenten für deinen neuen Sprachassistenten.\n'
      'In diesem Schritt Kannst du ein {}-Benutzerkonto einrichten.\n'
      'Dieser Setup-Assistent wird dich mit Fragen durch die Einrichtung führen.\n'
      'Bitte gib deine Antworten ein und bestätige sie mit [ENTER].\n'
      'Wenn du bei einer Frage die vorgegebene Standard-Antwort übernehmen willst, reicht es, wenn du einfach [ENTER] drückst, ohne etwas einzugeben.'.format(system_name))
time.sleep(1)
enterContinue()

print('\n')
user_name = frage_erfordert_antwort('Bitte gib einen Namen für diesen {}-Benutzer ein: '.format(system_name))
print('Okay, dieser Benutzer wird {} heißen.\n'.format(user_name))
time.sleep(1)

user_exists = False
if os.path.exists('server/users/' + user_name + '/User_Info.json'):
    user_exists = True
    print('Es wurde eine bestehende Konfiguration für den Nutzer {} gefunden.'.format(user_name))
    antwort = ja_nein_frage('Soll diese Konfiguration als Standardantworten geladen werden [Ja / Nein]? [Standard ist "Ja"]', True)
    if antwort == True:
        print('Konfiguration wird geladen...\n')
        with open('server/users/' + user_name + '/User_Info.json', 'r') as config_file:
            user_config_data = json.load(config_file)
    else:
        with open('server/resources/user_default/User_Info.json', 'r') as config_file:
            user_config_data = json.load(config_file)
else:
    with open('server/resources/user_default/User_Info.json', 'r') as config_file:
        user_config_data = json.load(config_file)

user_config_data['User_Info']['name'] = user_name
if not user_exists:
    subdirs = os.listdir('server/users')
    num_users = len(subdirs)
    user_config_data['User_Info']['uid'] = num_users + 1

default_role = user_config_data['User_Info']['role']
user_role = frage_mit_default('Bitte gib eine Berechtigungsstufe für den Nutzer "{}" ein (z.B. "USER" oder "ADMIN") [Standard ist "{}"]: '.format(user_name, default_role), default_role)
user_config_data['User_Info']['role'] = user_role
print('Okay, der Nutzer "{}" wird "{}" sein.\n'.format(user_name, user_role))
time.sleep(1)

if server_config_data['telegram']:
    default_id = user_config_data['User_Info']['telegram_id']
    telegram_id = frage_nach_zahl('Bitte gib die Telegram-ID-Nummer dieses Nutzers ein (oder 0, wenn für diesen Nutzer kein Telegram-Zugang eingerichtet werden soll). '
                                  'Tipp: Um deine ID herauszufinden, kannst du deinen Sprachassistenten einfach schon mal anschreiben und die ID aus der unvermeidlichen '
                                  'Fehlermeldung entnehmen. [Standard ist "{}"]: '.format(default_id), default_id)
    user_config_data['User_Info']['telegram_id'] = telegram_id
    if telegram_id == 0:
        print('Okay, für diesen Nutzer wird kein Telegram-Zugang eingerichtet.\n')
    else:
        print('Okay, {} wird den Nutzer "{}" an der Telegram-ID "{}" erkennen.\n'.format(system_name, user_name, telegram_id))
    time.sleep(1)

print('Die wichtigsten Schritte zur Einrichtung dieses Nutzers sind damit abgeschlossen.\n'
      'Im Anschluss werden nun noch einige persönliche Daten über den Nutzer abgefragt, die von bestimmten Modulen verwendet werden.\n'
      'Wenn du zu einer Frage keine Angaben machen möchtest, kannst du auch einfach [ENTER] drücken, ohne etwas einzugeben.\n'
      'Die allermeisten {}-Module werden auch ohne diese Informationen problemlos funktionieren.'.format(system_name))
time.sleep(1)
enterContinue()

default_first_name = user_config_data['User_Info']['first_name']
if not default_first_name == '':
    first_name = frage_mit_default('\nBitte gib deinen vollen Vornamen ein [Standard ist "{}"]: '.format(default_first_name), default_first_name)
else:
    first_name = input('\nBitte gib deinen vollen Vornamen ein: ')
user_config_data['User_Info']['first_name'] = first_name
time.sleep(1)

default_last_name = user_config_data['User_Info']['last_name']
if not default_last_name == '':
    last_name = frage_mit_default('\nBitte gib deinen vollen Nachnamen ein [Standard ist "{}"]: '.format(default_last_name), default_last_name)
else:
    last_name = input('\nBitte gib deinen vollen Nachnamen ein: ')
user_config_data['User_Info']['last_name'] = last_name
time.sleep(1)

default_bday_year = user_config_data['User_Info']['date_of_birth']['year']
if not default_bday_year == 0:
    bday_year = frage_nach_zahl('\nBitte gib dein Geburtsjahr ein (als ganze Jahreszahl, z.B. "1970") [Standard ist "{}"]: '.format(default_bday_year), default_bday_year)
else:
    bday_year = frage_nach_zahl('\nBitte gib dein Geburtsjahr ein (als ganze Jahreszahl, z.B. "1970"): ', default_bday_year)
user_config_data['User_Info']['date_of_birth']['year'] = bday_year
time.sleep(1)

default_bday_month = user_config_data['User_Info']['date_of_birth']['month']
if not default_bday_month == 0:
    bday_month = frage_nach_zahl('\nBitte gib deinen Geburtsmonat ein (als Zahl, z.B. "01") [Standard ist "{}"]: '.format(default_bday_month), default_bday_month)
else:
    bday_month = frage_nach_zahl('\nBitte gib deinen Geburtsmonat ein (als Zahl, z.B. "01"): ', default_bday_month)
user_config_data['User_Info']['date_of_birth']['month'] = bday_month
time.sleep(1)

default_bday_day = user_config_data['User_Info']['date_of_birth']['day']
if not default_bday_day == 0:
    bday_day = frage_nach_zahl('\nBitte gib deinen Geburtstag ein (als Zahl, z.B. "30") [Standard ist "{}"]: '.format(default_bday_day), default_bday_day)
else:
    bday_day = frage_nach_zahl('\nBitte gib deinen Geburtstag ein (als Zahl, z.B. "30"): ', default_bday_day)
user_config_data['User_Info']['date_of_birth']['day'] = bday_day
time.sleep(1)

end_config(user_config_data, system_name)
