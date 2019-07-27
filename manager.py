#A manager script.
#Starts both the bot (main.py) and the webconfig (Webconfig/__init__.py)

import subprocess

p = subprocess.Popen("flask run", cwd=r"C:\Users\luukv\Documents\#Programming\Python\Tsuyu Asui\Webconfig") #webconfig
print(p)

import main #bot
