import json
import requests
import argparse
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")

#chrome_options.add_argument("--disable-gpu")

chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

class BotVictim:

    def __init__(self, url):
        self.url_to_connect = url
        self.my_server_ip_address = str(os.getenv("SERVER_IP_ADDRESS"))
        self.url_server =  "http://10.0.0.3/" # "http://" + self.my_server_ip_address + "/"
        self.my_user = "local@host.gouv" # str(os.getenv("BOT_ID"))
        self.my_pw = "kikou" # str(os.getenv("BOT_PW"))

    def login(self):
        ses = requests.Session()
        res = ses.post(
            url=self.url_server + "auth/login",
            json = {
                "email": self.my_user,
                "password": self.my_pw
            }
        )
        json_data = res.json()
        self.token = str(json_data['Authorization'])
    
    def go_to_the_url(self):
        driver.get("https://google.com")
        cookies_dict = {
            "name": 'wowo',
            'value': self.token
        }
        print(driver.page_source.encode("utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="the scenario/config name")
    args = parser.parse_args()


    if args.url:
        bot = BotVictim(args.url)
        bot.login()
        bot.go_to_the_url()
    else:
        print("You must mention an url.")
        sys.exit(1)