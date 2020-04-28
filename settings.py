import os
import importlib
import imp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings_dev_path = BASE_DIR+"/settings_dev.py"


if not os.path.isfile(settings_dev_path):
    f = open(settings_dev_path, 'w+')
    f.write('from settings_dist import *\n\n')
    f.write('# This file will override settings_dist\n')
    f.write('# FILENAME = \'my-questions.csv\'\n')
    f.close()

settings_module = os.getenv('SETTINGS_MODULE', None)
if settings_module:
    settings = importlib.import_module(settings_module)
else:
    settings = imp.load_source("settings_dev", settings_dev_path)
