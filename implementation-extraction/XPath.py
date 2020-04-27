import readFiles
import json
import re
from lxml import html
from pathlib import Path

data_folder = Path("WebPages/")


def process_xpath(page_content, type):
    tree = html.fromstring(str(page_content))

    if type == 'rtvslo':
        data = {'author': tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[1]/div/text()')[0],
                'publilshedTime': tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[2]/text()[1]')[0],
                'title': tree.xpath('//*[@id="main-container"]/div[3]/div/header/h1/text()')[0],
                'subTitle': tree.xpath('//*[@id="main-container"]/div[3]/div/header/div[2]/text()')[0],
                'lead': tree.xpath('//*[@id="main-container"]/div[3]/div/header/p/text()')[0],
                'content': ' '.join(tree.xpath('//*[@id="main-container"]/div[3]/div/div[2]/article/p/text()'))}
    elif type == 'RačunalniškeNovice':
        data = {'category': ' -> '.join(tree.xpath('//*[@id="whole-path"]/a/text()')),
                'subCategory': tree.xpath('//*[@id="content-holder"]/div[3]/div[1]/div[3]/div[3]/text()')[0],
                'publilshedTime': tree.xpath('//*[@id="content-holder"]/div[3]/div[1]/div[3]/div[1]/text()')[0],
                'title': tree.xpath('//*[@id="_iprom_inStream"]/h1/text()')[0],
                'subTitle': ', '.join(tree.xpath('//*[@id="single-art-text"]/p/strong/text()')),
                'content': ' '.join(tree.xpath('//*[@id="single-art-text"]/p/text()'))}
    elif type == 'overstock':
        data = {}

        titles = tree.xpath(
            '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a/b/text()')
        contents = tree.xpath(
            '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/span/text()')
        list_prices = tree.xpath(
            '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/s/text()')
        prices = tree.xpath(
            '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/span/b/text()')
        savings = tree.xpath(
            '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span/text()')

        i = 0
        for title in titles:
            data[title] = {
                'title': titles[i],
                'content': contents[i],
                'listPrice': list_prices[i],
                'price': prices[i],
                'saving': savings[i].split(' ')[0],
                'savingPercent': re.findall("(?<=\().+?(?=\))", savings[i].split(' ')[1])[0]
            }
            i += 1

    elif type == 'ceneje':
        data = {}
        title = tree.xpath('//*[@id="mainContent"]/div[4]/h1/text()')[0]
        sellers = tree.xpath('//*[@id="offersList"]/div/div[2]/div[1]/a/img/@alt')
        prices = tree.xpath('//*[@id="offersList"]/div/div[2]/div[3]/div[2]/a/text()')
        ratings = tree.xpath('//*[@id="offersList"]/div/div[3]/a/div/div[2]/span/text()')
        print(prices)
        i = 0
        for seller in sellers:
            data['title'] = title
            lprice = tree.xpath('//*[@id="offersList"]/div[' + str(i+1) + ']/div[2]/div[3]/div[2]/div/span[2]/text()')
            if lprice:
                lprice = re.findall('(\d+\,?\d*)', lprice[0])[0]
            saving = tree.xpath('//*[@id="offersList"]/div[' + str(i+1) + ']/div[2]/div[3]/div[2]/div/span[1]/text()')
            if saving:
                saving = re.findall('\d+', saving[0])[0]

            data[seller] = {
                'seller': seller,
                'listPrice': lprice,
                'price': prices[i],
                'numRatings': ratings[i],
                'savingPercent': saving
            }
            i += 1

    print(data)
    return data


def saveToFile(fileName, data):
    with open(data_folder / fileName, 'w') as outfile:
        json.dump(data, outfile)


def process():
    print("STARTED PROCESSING RTVSLO")
    res1 = process_xpath(readFiles.rtvslo1, 'rtvslo')
    saveToFile("XPath-rtvslo-output.json", res1)

    print("STARTED PROCESSING RačunalniškeNovice")
    res2 = process_xpath(readFiles.RacNovice1, 'RačunalniškeNovice')
    saveToFile("XPath-racNovice-output.json", res2)

    print("STARTED PROCESSING OVERSTOCK")
    res3 = process_xpath(readFiles.overstock1, 'overstock')
    saveToFile("XPath-overstock-output.json", res3)

    print("STARTED PROCESSING CENEJE.SI")
    res4 = process_xpath(readFiles.ceneje3, 'ceneje')
    saveToFile("XPath-ceneje-output.json", res4)
