from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import concurrent.futures
import threading
import psycopg2
from urllib import parse
from urllib import robotparser
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time

profile = webdriver.FirefoxProfile()
AGENT_NAME = 'frie-ieps-11'
profile.set_preference("general.useragent.override", AGENT_NAME)
DISALLOWED = []
frontier = ["https://evem.gov.si", "https://gov.si",
            "https://evem.gov.si",
            "https://e-uprava.gov.si",
            "https://e-prostor.gov.si"]

lock = threading.Lock()

options = Options()
options.headless = True
driver = webdriver.Firefox(profile,options=options)

def validUrl(url):
    for i in DISALLOWED:
        if "gov.si"+i in url:
            return False
    return not url in frontier and "gov.si" in url

def crawler(path):
    try:
        driver.get(path)

        time.sleep(2)
        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            if validUrl(elem.get_attribute("href")):
                frontier.append(elem.get_attribute("href"))

        print(frontier)

    except TimeoutException:
        driver.quit()
        print('MOVIE NOT YET AVAILABLE!')
        pass
    except:
        driver.quit()
        raise


def nit(counter_id, increases):
    # conn = psycopg2.connect(host="localhost", user="user", password="SecretPassword")
    # conn.autocommit = True

    while frontier:
        with lock:
            crawler(frontier.__getitem__(0))
            frontier.pop(0)
            # print("id: " + counter_id, end=" ")
            # print(counter_id)
            # cur = conn.cursor()
            # cur.execute("SELECT value FROM showcase.counters WHERE counter_id = %s", \
            #             (counter_id,))
            # value = cur.fetchone()[0]
            # cur.execute("UPDATE showcase.counters SET value = %s WHERE counter_id = %s", \
            #             (value + 1, counter_id))
            # cur.close()
    # conn.close()


def readRobotTxt():
    parser = robotparser.RobotFileParser()
    parser.set_url(parse.urljoin("https://gov.si/", 'robots.txt'))
    parser.read()
    for i in parser.default_entry.rulelines:
        DISALLOWED.append(i.path)


def main():
    while True:
        val = input("Vnesite število željenih niti (1-10): ")
        if int(val) <= 10 and int(val) >= 1:
            break
    readRobotTxt()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(int(val)):
            executor.submit(nit, i, 1)


if __name__ == "__main__":
    main()
