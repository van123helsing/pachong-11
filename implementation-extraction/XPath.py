import readFiles
import json
from lxml import html
from pathlib import Path

data_folder = Path("WebPages/")


def process_xpath(page_content, type):
    tree = html.fromstring(str(page_content))

    if type == 'rtvslo':
        tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[1]/div/text()')
        data = {'author': tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[1]/div/text()')[0],
                'publilshedTime': tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[2]/text()[1]')[0],
                'title': tree.xpath('//*[@id="main-container"]/div[3]/div/header/h1/text()')[0],
                'subTitle': tree.xpath('//*[@id="main-container"]/div[3]/div/header/div[2]/text()')[0],
                'lead': tree.xpath('//*[@id="main-container"]/div[3]/div/header/p/text()')[0],
                'content': ' '.join(tree.xpath('//*[@id="main-container"]/div[3]/div/div[2]/article/p/text()'))}
    elif type == 'RačunalniškeNovice':
        #TODO: fix xpath
        tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[1]/div/text()')
        data = {'author': tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[1]/div/text()')[0],
                'publilshedTime': tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[2]/text()[1]')[0],
                'title': tree.xpath('//*[@id="_iprom_inStream"]/h1/text()')[0],
                'subTitle': tree.xpath('//*[@id="main-container"]/div[3]/div/header/div[2]/text()')[0],
                'lead': tree.xpath('//*[@id="main-container"]/div[3]/div/header/p/text()')[0],
                'content': ' '.join(tree.xpath('//*[@id="main-container"]/div[3]/div/div[2]/article/p/text()'))}

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

    # print("STARTED PROCESSING OVERSTOCK")
    # res3 = process_xpath(readFiles.overstock1)
    # saveToFile("XPath-overstock-output.json", res3)
    #
    # print("STARTED PROCESSING CENEJE.SI")
    # res4 = process_xpath(readFiles.ceneje1)
    # saveToFile("XPath-ceneje-output.json", res4)

