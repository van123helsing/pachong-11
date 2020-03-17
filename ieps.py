from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import concurrent.futures
import threading
from urllib import parse
from urllib import robotparser
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests
import re
import time
import db
import models

profile = webdriver.FirefoxProfile()
AGENT_NAME = 'fri-ieps-11'
profile.set_preference("general.useragent.override", AGENT_NAME)
DISALLOWED = []
root = ["https://gov.si",
        "https://evem.gov.si",
        "https://e-uprava.gov.si",
        "https://e-prostor.gov.si"]
frontier = ["https://gov.si",
            "https://evem.gov.si",
            "https://e-uprava.gov.si",
            "https://e-prostor.gov.si"]

lock = threading.Lock()

options = Options()
options.headless = True
options.add_argument("user-agent=" + AGENT_NAME)
driver = webdriver.Firefox(profile, options=options)

dbConn = db.DataBase()


def valid_url(url):
    for i in DISALLOWED:
        if "gov.si" + i in url:
            return False
    return url not in frontier and "gov.si" in url


def crawler(path):
    try:
        driver.get(path)

        time.sleep(2)
        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            if valid_url(elem.get_attribute("href")):
                frontier.append(elem.get_attribute("href"))

        print(frontier)

        imgs = driver.find_elements_by_xpath("//img[@src]")
        for img in imgs:
            img_url = img.get_attribute("src")
            if "http" in img_url:
                img_name = img_url.split('/')[-1]
                r = requests.get(img_url, stream=True)  # downloading
                with open('./img/%s.png' % img_name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=128):
                        f.write(chunk)
                print('Saved %s' % img_name)


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


def read_site(site):
    # save current site to database
    robots = ""
    try:
        rp = robotparser.RobotFileParser()
        rp.set_url(parse.urljoin(site, '/robots.txt'))
        rp.read()

        # add all disallowed pages to an array
        for i in rp.default_entry.rulelines:
            DISALLOWED.append(parse.urljoin(site, i.path))

        robots = rp.__str__()
    except:
        print("robots.txt does not exist!")
        pass

    sitemap = ""
    try:
        r = requests.get(parse.urljoin(site, '/sitemap.xml'))
        xml = r.text

        # add all urls from sitemap to frontier
        soup = BeautifulSoup(xml, features="html.parser")
        sitemap_tags = soup.find_all("sitemap")
        if len(sitemap_tags) > 0:
            sitemap = xml
        for s in sitemap_tags:
            if valid_url(s.findNext("loc").text):
                frontier.append(s.findNext("loc").text)  # s.findNext("lastmod").text to get last modified date
    except:
        print("sitemap.xml does not exist!")
        pass

    dbConn.insert_site(models.Site(site, robots, sitemap))
    print("Inserted data for site " + site)
    time.sleep(2)


def main():
    while True:
        val = input("Vnesite število željenih niti (1-10): ")
        if val.isdigit() and 10 >= int(val) >= 1:
            break

    dbConn.empty_database()

    # check robots.txt file for all root domains
    for site in root:
        read_site(site)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(int(val)):
            executor.submit(nit, i, 1)


if __name__ == "__main__":
    main()
