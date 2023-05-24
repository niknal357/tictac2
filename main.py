import os
import json
import subprocess
import sys
import importlib.util
import random
from shutil import move


def version_compare(v1, v2):
    v1 = v1.split('.')
    v2 = v2.split('.')
    for i in range(min(len(v1), len(v2))):
        if int(v1[i]) > int(v2[i]):
            return 1
        elif int(v1[i]) < int(v2[i]):
            return -1
    if len(v1) > len(v2):
        return 1
    elif len(v1) < len(v2):
        return -1
    return 0


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_params(filename):
    extension = filename.split('.')[-1]
    with open(filename, 'r') as f:
        lines = f.readlines()
    params = {}
    if extension == 'py':
        comment = '#'
    elif extension == 'bat':
        comment = '::'
    else:
        print('Unknown extension: ' + extension)
        return params
    for lin in lines:
        line = lin.strip()
        if line == '':
            continue
        if not line.startswith(comment):
            break
        line = line.split(comment)[1:]
        line = comment.join(line)
        if ':' not in line:
            break
        values = line.split(':')
        if len(values) != 2:
            continue
        params[values[0].strip()] = values[1].strip()
    return params


if not os.path.exists('plugins/'):
    os.makedirs('plugins/')

subprocess.run(['curl', '-H', "'Cache-Control: no-cache, no-store'", 'https://raw.githubusercontent.com/niknal357/tictac2/main/file_reference.json',
               '-o', 'file_reference.json'], shell=True)

with open('file_reference.json', 'r') as f:
    files = json.loads(f.read())
to_dl = []
for filedata in files:
    if not os.path.exists(filedata['file']):
        to_dl.append(filedata)
        continue
    params = read_params(filedata['file'])
    if 'version' not in params:
        to_dl.append(filedata)
        continue
    if version_compare(params['version'], filedata['version']) < 0:
        to_dl.append(filedata)
        continue
for filedata in to_dl:
    print('Downloading ' + filedata['file'] + '...')
    subprocess.run(['curl', '-H', "'Cache-Control: no-cache, no-store'", filedata['url'], '-o',
                   'dl'], shell=True)
    move('dl', filedata['file'])

launcher = None
engine = None
bots = [{'name': 'Human', 'func': None}]


for mod in os.listdir('plugins'):
    if mod.split('.')[-1] != 'py':
        continue
    with open('plugins/' + mod, 'r') as f:
        lines = f.readlines()
    firstline = lines[0].strip('#').strip()
    if firstline.split(':')[0].strip() == 'mod_type':
        mod_type = firstline.split(':')[1].strip()
    else:
        continue
    if mod_type == 'launcher':
        launcher = module_from_file(
            mod, 'plugins/'+mod).launcher
    elif mod_type == 'engine':
        engine = module_from_file(
            mod, 'plugins/'+mod).engine
    elif mod_type == 'bot':
        secondline = lines[1].strip('#').strip()
        if secondline.split(':')[0].strip() == 'bot_name':
            bot_name = secondline.split(':')[1].strip()
        else:
            continue
        bots.append({'name': bot_name, 'func': module_from_file(
            mod, 'plugins/'+mod).bot})

if launcher == None:
    print('No launcher found, downloading default...')
    subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/plugins/default_launcher.py',
                   '-o', 'plugins/default_launcher.py'], shell=True)
    launcher = module_from_file(
        'default_launcher.py', 'plugins/default_launcher.py').launcher
if engine == None:
    print('No engine found, downloading default...')
    subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/plugins/default_engine.py',
                   '-o', 'plugins/default_engine.py'], shell=True)
    engine = module_from_file(
        'default_engine.py', 'plugins/default_engine.py').engine

# if True:
#    print('You seem to have no bots installed.')
#    #inp = input('would you like to install the default set of bots? (y/n) ')
#    if True:
#        subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/avajaris.py', '-o', 'plugins/avajaris.py'], shell=True)
#        subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/bot_3.py', '-o', 'plugins/bot_3.py'], shell=True)
#        subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/bot_7.py', '-o', 'plugins/bot_7.py'], shell=True)
#        subprocess.run(['curl', 'https://raw.githubusercontent.com/niknal357/tictac2/main/bot_8.py', '-o', 'plugins/bot_8.py'], shell=True)
#        for mod in os.listdir('plugins'):
#            if mod.split('.')[-1] != 'py':
#                continue
#            with open('plugins/' + mod, 'r') as f:
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
#                    mod, 'plugins/'+mod).bot})


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
