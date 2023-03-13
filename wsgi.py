print("This program is only for educational purposes!")

from flask import Flask, jsonify, request
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import threading
import requests
import uuid
import time
import sys


def is_valid_uuid(uu, v=4):
    try:
        uuu = uuid.UUID(uu, version=v)
    except ValueError:
        return False
    return str(uuu) == uu # uuu uu uuuuuu

def get_usernames(query):
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("start-maximized")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    
    print("Connecting to NameMC...")
    driver.get("https://namemc.com/")
    time.sleep(5)

    print("Searching UUID ("+query+")...")
    searchBox = driver.find_element(By.ID, "search-box")
    searchBox.send_keys(query)
    searchBox.send_keys(Keys.ENTER)

    time.sleep(5)
    print("Waiting for results...")
    usernameLinks = driver.find_elements(By.XPATH, "//a[@href]")
    print("Found potential results!")

    usernames = []

    for link in usernameLinks:
        href = link.get_attribute("href")
        if "search?q=" in href:
            usernames.append(href.split("?q=")[1])
            print("Found username ("+usernames[-1]+")!", flush=True)

    driver.close()

    with open('cache.csv', 'a') as f:
        f.write(query + "," + ",".join(usernames) + "\n")


app = Flask(__name__)
thread = threading.Thread()
currentProcesses = []


@app.route("/")
def hello():
    ip = request.headers["X-Forwarded-For"]
    return f"<h1>Go away</h1><p>srsly go away {ip}</p>"
  

@app.route('/name_history/<string:uu>', methods = ['GET'])
def name_history(uu):
    print("Validating UUID ("+uu+")...", flush=True)

    if (is_valid_uuid(uu)):
        query = uu
    else:
        return jsonify({'error': 'incorrect_uuid'})
        
    with open('cache.csv', 'r') as f:
        for line in f:
            if query == line.split(",")[0]:
                return jsonify({'uuid':query,'usernames': line.replace("\n", "").split(",")[1:]})
    
    if uu not in currentProcesses:
        thrd = threading.Thread(target=get_usernames, args=(query,))
        thrd.start()
        currentProcesses.append(query)
    
    return jsonify({'status':'in_progress'})


@app.route('/entire_name_history/')
def entire_name_history():
    acc = []

    with open ('cache.csv', 'r') as f:
        for line in f:
            if "," in line:
                acc.append({'uuid':line.split(",")[0],'usernames': line.replace("\n", "").split(",")[1:]})

    return jsonify({'users':acc})

  
if __name__ == '__main__':
    app.run(debug = True)
