import readFiles
import json
import re
from lxml import html
from pathlib import Path

data_folder = Path("WebPages/output/XPath/")


def process_xpath(page_content, type):
    parser = html.HTMLParser()
    tree = html.fromstring(str(page_content), parser=parser)

    if type == 'rtvslo':
        data = {'author': tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[1]/div/text()')[0],
                'publishedTime': tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[2]/text()[1]')[0],
                'title': tree.xpath('//*[@id="main-container"]/div[3]/div/header/h1/text()')[0],
                'subTitle': tree.xpath('//*[@id="main-container"]/div[3]/div/header/div[2]/text()')[0],
                'lead': tree.xpath('//*[@id="main-container"]/div[3]/div/header/p/text()')[0],
                'content': ' '.join(tree.xpath('//*[@id="main-container"]/div[3]/div/div[2]/article/p/text()'))}
    elif type == 'RačunalniškeNovice':
        data = {'category': ' -> '.join(tree.xpath('//*[@id="whole-path"]/a/text()')),
                'subCategory': tree.xpath('//*[@id="content-holder"]/div[3]/div[1]/div[3]/div[3]/text()')[0],
                'publishedTime': tree.xpath('//*[@id="content-holder"]/div[3]/div[1]/div[3]/div[1]/text()')[0],
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

        data['category'] = tree.xpath('//*[@id="mainContent"]/div[3]/h1/text()')[0]
        data['numberOfListings'] = tree.xpath('//*[@id="mainContent"]/div[6]/div[2]/div[1]/div[1]/b/text()')[0]
        titles = tree.xpath('//*[@id="productGrid"]/div/div/div[2]/h3/a/text()')
        prices = tree.xpath('//*[@id="productGrid"]/div/div/div[2]/p/a[1]/b/text()')
        stores = tree.xpath('//*[@id="productGrid"]/div/div/div[2]/p/a[2]/b/text()')

        i = 0
        for title in titles:
            data[title] = {
                'title': titles[i],
                'price': prices[i].split(' ')[0],
                'stores': max(stores[i].split(' '), key=len) if max(stores[i].split(' '), key=len) != "trgovinah\n" else "Več trgovin"
            }
            i += 1

    # print(data)
    return data


def saveToFile(fileName, data):
    with open(data_folder / fileName, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def process():
    print("STARTED PROCESSING RTVSLO")
    res1 = process_xpath(readFiles.rtvslo1, 'rtvslo')
    saveToFile("rtvslo1.json", res1)
    res2 = process_xpath(readFiles.rtvslo2, 'rtvslo')
    saveToFile("rtvslo2.json", res2)

    print("STARTED PROCESSING RačunalniškeNovice")
    res3 = process_xpath(readFiles.RacNovice1, 'RačunalniškeNovice')
    saveToFile("RacNovice1.json", res3)
    res4 = process_xpath(readFiles.RacNovice2, 'RačunalniškeNovice')
    saveToFile("RacNovice2.json", res4)

    print("STARTED PROCESSING OVERSTOCK")
    res5 = process_xpath(readFiles.overstock1, 'overstock')
    saveToFile("overstock1.json", res5)
    res6 = process_xpath(readFiles.overstock2, 'overstock')
    saveToFile("overstock2.json", res6)

    print("STARTED PROCESSING CENEJE.SI")
    res7 = process_xpath(readFiles.ceneje1, 'ceneje')
    saveToFile("ceneje1.json", res7)
    res8 = process_xpath(readFiles.ceneje2, 'ceneje')
    saveToFile("ceneje2.json", res8)
