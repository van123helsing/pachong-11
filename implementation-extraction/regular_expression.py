import json
import re
from lxml import html
from pathlib import Path


data_folder = Path("WebPages/output/RegularExpression")


def process_regex(page_content, type):
    if type == 'rtvslo':
        data = {
            "author" : re.compile( r"<div class=\"author-name\">([a-zA-Z]+\s+[a-zA-Z]+)").search(page_content).group(1),
            "publishedTime" : re.compile( r"<div class=\"publish-meta\">\s+([0-9]*.\s+[a-z]+\s+[0-9]*\s+[a-z]+\s+[0-9]+\:[0-9]+)").search(page_content).group(1),
            "title" :  re.compile( r"<header class=\"article-header\">[\s\S]+?<h1>([\s\S]+?)<\/h1>[\s\S]+?<\/header>").search(page_content).group(1),
            "subTitle" : re.compile( r"<header class=\"article-header\">[\s\S]+?<div class=\"subtitle\">([\s\S]+?)<\/div>[\s\S]+?<\/header>").search(page_content).group(1),
            "lead" : re.compile( r"<header class=\"article-header\">[\s\S]+?<p class=\"lead\">([\s\S]+?)<\/p>[\s\S]+?<\/header>").search(page_content).group(1),
            "content" : re.compile( r"<div class=\"article-body\">[\s\S]+?<article class=\"article\">([\s\S]+?)<\/article>[\s\S]+?<\/div>").search(page_content).group(1),
        }
    elif type == 'overstock':
        data = {}
        titles = re.findall(r"<tr bgcolor=\"#[f|d]+\">[\S\s]*?<a href=\"http://www\.overstock\.com/cgi-bin/d2\.cgi\?PAGE=PROFRAME&amp;PROD_ID=[0-9]+?\"><b>([\S\s]+?)<\/b>", page_content)
        # for name in titles:
        #     print(name)
        listPrices = re.findall(r"<tr bgcolor=\"#[f|d]+\">[\S\s]*?<b>List Price:<\/b>[\S\s]*?<s>(.*?)<\/s>", page_content)
        prices = re.findall(r"<tr bgcolor=\"#[f|d]+\">[\S\s]*?<b>Price:<\/b>[\S\s]*?<b>(.*?)<\/b>", page_content)
        savings = re.findall(r"<tr bgcolor=\"#[f|d]+\">[\S\s]*?<b>You Save:<\/b>[\S\s]*?<span class=\"littleorange\">(.*?) \(.*?\)<\/span>", page_content)
        savingPercents = re.findall(
            r"<tr bgcolor=\"#[f|d]+\">[\S\s]*?<b>You Save:<\/b>[\S\s]*?<span class=\"littleorange\">.*? \((.*?)\)<\/span>",
            page_content)
        contents = re.findall(
            r"<tr bgcolor=\"#[f|d]+\">[\S\s]*?<a href=\"http://www\.overstock\.com/cgi-bin/d2\.cgi\?PAGE=PROFRAME&amp;PROD_ID=[0-9]+?\">[\S\s]*?<span class=\"normal\">([\S\s]*?)<br>",
            page_content)
        # for i in contents:
        #     print(i)
        j = 0
        for title in titles:
            data[title] = {
                'title': titles[j],
                'listPrice': listPrices[j],
                'price': prices[j],
                'saving': savings[j],
                'savingPercent':  savingPercents[j],
                'content': contents[j]
            }
            j += 1

    #print(data)
    return data



def saveToFile(fileName, data):
    with open(data_folder / fileName, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

def process():

    rtvslo1 = open('Webpages/Audi.html','r', encoding='utf8').read()
    rtvslo1_data = process_regex(rtvslo1,"rtvslo")
    saveToFile("Re-rtv1-output.json", rtvslo1_data)

    rtvslo2 = open('Webpages/Volvo.html','r', encoding='utf8').read()
    rtvslo2_data = process_regex(rtvslo2,"rtvslo")
    saveToFile("Re-rtv2-output.json", rtvslo2_data)

    rac_novice1 = open('Webpages/RacNovice1.html','r', encoding='utf8').read()
    rac_novice1_data = process_regex(rac_novice1,"rac_novice1")
    #saveToFile("Re-racNovice-output.json", rac_novice1_data)

    # rac_novice2 = open('Webpages/RacNovice2.html','r', encoding='utf8').read()
    # rac_novice2_data = process_regex(rac_novice2,"rac_novice2")
    # saveToFile("Re-racNovice-output.json", rac_novice2_data)

    overstock1 = open('WebPages/jewelry01.html','r', encoding='utf-8', errors='ignore').read()
    doverstock1_data = process_regex(overstock1, "overstock")
    saveToFile("Re-overstock1-output.json", doverstock1_data)

    overstock2 = open('WebPages/jewelry02.html','r', encoding='utf-8', errors='ignore').read()
    doverstock2_data = process_regex(overstock2, "overstock")
    saveToFile("Re-overstock2-output.json", doverstock2_data)








