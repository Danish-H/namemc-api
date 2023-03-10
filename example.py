print("This program is only for educational purposes!")

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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


options = uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument("start-maximized")
driver = uc.Chrome(options=options)

query = "3d45e14f-bdae-43a4-bc75-1919414db750" # my uwu id
usernames = []

if len(sys.argv) > 1:
    if (is_valid_uuid(sys.argv[1])):
        query = sys.argv[1]
    else:
        username = sys.argv[1]
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?")
        try:
            query = response.json()["id"]
        except:
            print("User", username, "does not exist or there is some issue with the API!")
            exit()

driver.get("https://namemc.com/")
driver.maximize_window()

time.sleep(10)
print("Searching UUID ("+query+")...")
searchBox = driver.find_element(By.ID, "search-box")
searchBox.send_keys(query)
searchBox.send_keys(Keys.ENTER)

time.sleep(10)
print("Waiting for results...")
usernameLinks = driver.find_elements(By.XPATH, "//a[@href]")
print("Found potential results!")

for link in usernameLinks:
    href = link.get_attribute("href")
    if "search?q=" in href:
        usernames.append(href.split("?q=")[1])
        print("Found username ("+usernames[-1]+")!")

print("\nUsername history:")
for u in usernames:
    print(u)

driver.close()
