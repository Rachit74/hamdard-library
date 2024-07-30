import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(BASE_DIR, 'key.txt')

with open(KEY_FILE, 'r') as file:
    global key
    key = file.read()