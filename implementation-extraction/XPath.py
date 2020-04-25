# import requests
# import json
# from lxml import html
#
# pageContent = requests.get('https://www.rtvslo.si/kultura/vizualna-umetnost/transformatorske-postaje-kot-podlaga-muralom/521321')
# tree = html.fromstring(pageContent.content)
#
# dataJSON = {}
# dataJSON['author'] = tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[1]/div/text()')
# dataJSON['publilshedTime'] = tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[2]/text()[1]')
# dataJSON['title'] = tree.xpath('//*[@id="main-container"]/div[3]/div/header/h1/text()')
# dataJSON['subTitle'] = tree.xpath('//*[@id="main-container"]/div[3]/div/header/div[2]/text()')
# dataJSON['lead'] = tree.xpath('//*[@id="main-container"]/div[3]/div/header/p/text()')
# dataJSON['content'] = tree.xpath('//*[@id="main-container"]/div[3]/div/div[2]/article')
#
# print(dataJSON)
