import json
import os
import time

CHAT_FOLDER = 'chats'
FILE_NAME = 'chat.json'
file_path = os.path.join(CHAT_FOLDER, FILE_NAME)

def r_chat():
    
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return {}
    with open(file_path, "r") as file:
        #print(file)
        return json.load(file)

def w_chat(user, text):
    d = {}
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        d = {}
    else:
        with open(file_path, "r") as file:
            d =  json.load(file)
    #print(d)
    
    #print(d)
    d[str(time.time())] = {"user": user, "text": text}
    #print(d)
    with open(file_path, "w") as file:
        json.dump(d, file, indent=4)
    return True
# w_chat("user","hi")
# w_chat("bot","hi")
# w_chat("hero","hi")

