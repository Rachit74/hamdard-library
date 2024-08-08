import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(BASE_DIR, 'key.txt')

print(f"Looking for key file at: {KEY_FILE}")

with open(KEY_FILE, 'r') as file:
    key = file.read()
