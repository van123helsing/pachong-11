from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import concurrent.futures
import threading
from urllib import parse
from urllib import robotparser
from urllib.parse import urldefrag, urljoin, urlsplit
from html import unescape
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests
import re
import time
import db
import models
import sys
import hashlib
import enums
from datetime import datetime
from datetime import timedelta
import socket

profile = webdriver.FirefoxProfile()
AGENT_NAME = 'fri-ieps-11'
profile.set_preference("general.useragent.override", AGENT_NAME)
DISALLOWED = []
frontier = ["https://gov.si",
            "https://evem.gov.si",
            "https://e-uprava.gov.si",
            "https://e-prostor.gov.si"]

history = set()

lock = threading.Lock()

options = Options()
options.headless = True
options.add_argument("user-agent=" + AGENT_NAME)
driver = webdriver.Firefox(profile, options=options)
dbConn = db.DataBase()

timeouts = dict()


def is_timeout(ip):
    # izbrišemo IP iz seznama ce je potekel njegov timeout
    keys = list(timeouts.keys())
    values = list(timeouts.values())
    for i in range(len(keys)):
        if keys[i] == ip and datetime.now() > (values[i] - timedelta(milliseconds=300)):
            print("Deleting timeout for: ", ip)
            del timeouts[keys[i]]
    # ce IP-ja ni v seznamu, ne vrnemo timeouta
    if ip not in timeouts:
        return 0
    # IP je v seznamu, nastavimo timeout
    else:
        time = timeouts.get(ip)
        now = datetime.now()
        print("Wainting to send request to " + str(ip) + " for " + str((time - now).seconds) + " seconds.")
        return (time - now).seconds


def clear_www(url):
    if url.startswith('www.'):
        url = re.sub(r'www.', '', url)
    return url


def clean_link(url):
    if not url.startswith('http'):
        base_url = urljoin(driver.current_url, '.')
        url = base_url[:-1] + url

    url, frag = urldefrag(url)

    re.sub(":80/", "", url)

    # re.sub("index\.html$", "", url)

    url = unescape(url)

    url = url.replace(" ", "%20")

    sep = '/#'
    url = url.split(sep, 1)[0]

    return url


def valid_url(url):
    # da preprecimo pasti
    if len(url) > 200:
        return False
    # ostale kontrole pravilnega url-ja
    for i in DISALLOWED:
        if "gov.si" + i in url:
            return False
    return url not in frontier and url not in history and "gov.si" in url


def crawler(path):
    try:
        # nastavimo prazne objekte
        page = models.Page
        page_data = None

        ip = socket.gethostbyname(urlsplit(path).netloc)
        time.sleep(is_timeout(ip))
        driver.get(path)
        r = requests.head(driver.current_url)
        header = r.headers.get('content-type').split(";")[0]
        timeouts[ip] = datetime.now() + timedelta(seconds=5)

        time.sleep(2)  # za javscript, da se nalozi

        # pridobimo vsebino strani
        data = driver.page_source

        # hashamo za preverjanje ce smo ze obiskali isto stran z drugim url
        data_hash = hashlib.md5(data.encode())
        page.hash = data_hash.digest()
        h = dbConn.check_if_hash_exists(data_hash.digest())
        # http status koda
        page.http_status_code = r.status_code
        # cas dostopa
        page.accessed_time = datetime.now()
        # url
        page.url = driver.current_url

        # ali site se ni dodan
        page.site_id = dbConn.check_if_domain_exists(clear_www(urlsplit(driver.current_url).netloc))
        if page.site_id is None:
            page.site_id = read_site(driver.current_url)

        # hash ze obstaja v bazi
        if h is not None:
            # TODO DUPLICATE - dodaj page, poporavi talebo link
            page.page_type_code = enums.PageType.DUPLICATE.value
            page.html_content = ''
            dbConn.insert_link(models.Link(path), h)
            return
        # hash ne obstaja v bazi
        else:
            if header == 'text/html':
                page.page_type_code = enums.PageType.HTML.value
                page.html_content = data
            else:
                page.page_type_code = enums.PageType.BINARY.value
                page.html_content = ''
                page_data = models.PageData
                page_data.data_type_code = 'OTHER'
                page_data.data = ''
                if header == enums.MimeType.PDF:
                    page_data.data_type_code = enums.DataType.PDF.value
                elif header == enums.MimeType.DOC:
                    page_data.data_type_code = enums.DataType.DOC.value
                elif header == enums.MimeType.DOCX:
                    page_data.data_type_code = enums.DataType.DOCX.value
                elif header == enums.MimeType.PPT:
                    page_data.data_type_code = enums.DataType.PPT.value
                elif header == enums.MimeType.PPTX:
                    page_data.data_type_code = enums.DataType.PPTX.value

        page_id = dbConn.insert_page(page)
        if page_data is not None:
            page_data.page_id = page_id
            dbConn.insert_page_data(page_data)

        add_links()

        print(frontier)

        add_imgs()

    except TimeoutException:
        print('Webpage did not load in within the time limit.')
        pass
    except:
        print("Unexpected error:", str(sys.exc_info()))
        pass


def add_imgs():
    imgs = driver.find_elements_by_xpath("//img[@src]")
    for img in imgs:
        img_url = img.get_attribute("src")
        if "http" in img_url:
            img_name = img_url.split('/')[-1]
            r = requests.get(img_url, stream=True)
            # TODO ce sem prav prebral navodila ne rabimo shranjevat bytov-> sam metadata slike: decode
            # with open('./img/%s.png' % img_name, 'wb') as f:
            #     for chunk in r.iter_content(chunk_size=128):
            #         f.write(chunk)
            print('Saved %s' % img_name)


def add_links():
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        url = clean_link(elem.get_attribute("href"))
        if valid_url(url):
            frontier.append(elem.get_attribute("href"))


def nit(nit_id):
    while frontier:
        with lock:
            address = frontier.__getitem__(0)
            print("Thread " + str(nit_id) + ": STARTED: " + address)
            crawler(address)
            print("Thread " + str(nit_id) + ": FINISHED:  " + address)
            history.add(address)
            frontier.pop(0)
        time.sleep(1)


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

        robots = str(rp)
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

    print("Inserted data for site " + site)
    return dbConn.insert_site(models.Site(urlsplit(site).netloc, robots, sitemap))


def main():
    while True:
        val = input("Enter the number of desired threads (1-10): ")
        if val.isdigit() and 10 >= int(val) >= 1:
            break

    dbConn.empty_database()
    print("Database cleared.")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(int(val)):
            executor.submit(nit, i)


if __name__ == "__main__":
    main()
