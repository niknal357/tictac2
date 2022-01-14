import os
import json
import subprocess
import sys
import importlib.util
import random


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if not os.path.exists('mods/'):
    os.makedirs('mods/')

subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/bot_reference.json', '-o', 'bot_reference.json'], shell=True)
with open('bot_reference.json', 'r') as f:
    bots_to_download = json.loads(f.read())
for bot_to_download in bots_to_download:
    if bot_to_download['file'] not in os.listdir('mods/'):
        subprocess.run(['curl', bot_to_download['url'], '-o', 'mods/'+bot_to_download['file']])

launcher = None
engine = None
bots = [{'name': 'Human', 'func': None}]

for mod in os.listdir('mods'):
    if mod.split('.')[-1] != 'py':
        continue
    with open('mods/' + mod, 'r') as f:
        lines = f.readlines()
    firstline = lines[0].strip('#').strip()
    if firstline.split(':')[0].strip() == 'mod_type':
        mod_type = firstline.split(':')[1].strip()
    else:
        continue
    if mod_type == 'launcher':
        launcher = module_from_file(
            mod, 'mods/'+mod).launcher
    elif mod_type == 'engine':
        engine = module_from_file(
            mod, 'mods/'+mod).engine
    elif mod_type == 'bot':
        secondline = lines[1].strip('#').strip()
        if secondline.split(':')[0].strip() == 'bot_name':
            bot_name = secondline.split(':')[1].strip()
        else:
            continue
        bots.append({'name': bot_name, 'func': module_from_file(
            mod, 'mods/'+mod).bot})

if launcher == None:
    print('No launcher found, downloading default...')
    subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/default_launcher.py', '-o', 'mods/default_launcher.py'], shell=True)
    launcher = module_from_file(
        'default_launcher.py', 'mods/default_launcher.py').launcher
if engine == None:
    print('No engine found, downloading default...')
    subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/default_engine.py', '-o', 'mods/default_engine.py'], shell=True)
    engine = module_from_file(
        'default_engine.py', 'mods/default_engine.py').engine

#if True:
#    print('You seem to have no bots installed.')
#    #inp = input('would you like to install the default set of bots? (y/n) ')
#    if True:
#        subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/avajaris.py', '-o', 'mods/avajaris.py'], shell=True)
#        subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/bot_3.py', '-o', 'mods/bot_3.py'], shell=True)
#        subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/bot_7.py', '-o', 'mods/bot_7.py'], shell=True)
#        subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/bot_8.py', '-o', 'mods/bot_8.py'], shell=True)
#        for mod in os.listdir('mods'):
#            if mod.split('.')[-1] != 'py':  
#                continue
#            with open('mods/' + mod, 'r') as f:
#                lines = f.readlines()
#            firstline = lines[0].strip('#').strip()
#            if firstline.split(':')[0].strip() == 'mod_type':
#                mod_type = firstline.split(':')[1].strip()
#            else:
#                continue
#            if mod_type == 'bot':
#                secondline = lines[1].strip('#').strip()
#                if secondline.split(':')[0].strip() == 'bot_name':
#                    bot_name = secondline.split(':')[1].strip()
#                else:
#                    continue
#                bots.append({'name': bot_name, 'func': module_from_file(
#                    mod, 'mods/'+mod).bot})


while True:
    res = launcher(bots)
    if res == 'quit':
        break
    if len(res) == 2:
        res = engine(res[0], res[1], (20, 20))
    else:
        res = engine(res[0], res[1], (20, 20), res[2])
    if res == 'quit':
        break
    elif res == 'launcher':
        continue
