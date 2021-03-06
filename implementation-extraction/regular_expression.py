import json
import re
import regex
from pathlib import Path



data_folder = Path("input-extraction/output/RegularExpression/")

def convertArray(a):
    str = " ".join(a)
    return str


def process_regex(page_content, type):

    if type == 'rtvslo':

        content_matches = regex.compile(r"<article class=\"article\">[\s\S]*?(<p[\s\S]*?>([\s\S]*?)<\/p[\s\S]*?>[\s\S]*?)*<\/article>").finditer(page_content)
        content = ""
        #print(content_matches)
        for i in content_matches:
            for capture in i.captures(2):
                #print(capture)
                content += capture

        #print(content)

        data = {
            "author" : re.compile( r"<div class=\"author-name\">([a-zA-Z]+\s+[a-zA-Z]+)").search(page_content).group(1),
            "publishedTime" : re.compile( r"<div class=\"publish-meta\">\s+([0-9]*.\s+[a-z]+\s+[0-9]*\s+[a-z]+\s+[0-9]+\:[0-9]+)").search(page_content).group(1),
            "title" :  re.compile( r"<header class=\"article-header\">[\s\S]+?<h1>([\s\S]+?)<\/h1>[\s\S]+?<\/header>").search(page_content).group(1),
            "subTitle" : re.compile( r"<header class=\"article-header\">[\s\S]+?<div class=\"subtitle\">([\s\S]+?)<\/div>[\s\S]+?<\/header>").search(page_content).group(1),
            "lead" : re.compile( r"<header class=\"article-header\">[\s\S]+?<p class=\"lead\">([\s\S]+?)<\/p>[\s\S]+?<\/header>").search(page_content).group(1),
            "content" : content
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

    elif type == 'rac_novice':


        # a1 = re.compile(r"<div class=.*? id=\"single-art-text\">([\s\S]*?)<div class=\"mt10\" id=\"fb-root\">").search(page_content).group()
        # b1 = "".join(a1)
        # c1 = re.sub('<[^<]+?>', '', b1).replace('\n', '').strip()
        # print(c1)

        content_match = regex.compile(r"<div .*? id=\"single-art-text\">[\s\S]*?(<p[\s\S]*?>(<.*?>)?([\s\S]*?)(<.*?>)?<\/p[\s\S]*?>[\s\S]*?)*<div .*? id=\"fb-root\">").finditer(page_content)
        content = ""
        for z in content_match:
            for capture in z.captures(3):
                #print(capture)
                content += capture

        #print(content)

        data = {
            "category" : re.compile( r"<div id=\"whole-path\" class=\"intextAdIgnore\">[\S\s]*?<a href=.*?>(.*?)<\/a>[\S\s]*?<a href=.*?>(.*?)<\/a>").search(page_content).group(1) + " -> " + re.compile( r"<div id=\"whole-path\" class=\"intextAdIgnore\">[\S\s]*?<a href=.*?>(.*?)<\/a>[\S\s]*?<a href=.*?>(.*?)<\/a>").search(page_content).group(2),
            "subCategory" : re.compile( r"<div class=\"ml10 single-art-author fl\">(.*?)</div>").search(page_content).group(1),
            "publishedTime" :  re.compile( r"<div class=\"single-art-date fl mr10\">([\s\S]*?)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;([\s\S]*?)<\/div>").search(page_content).group(1)+ " " +re.compile( r"<div class=\"single-art-date fl mr10\">([\s\S]*?)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;([\s\S]*?)<\/div>").search(page_content).group(2),
            "title" : re.compile( r"<h1 class=\"h1 news-title-redesign intextAdIgnore\">(.*?)<\/h1>").search(page_content).group(1),
            "subTitle" : convertArray(re.compile( r"<p><strong>(.*?)<\/strong><\/p>").findall(page_content)),
            "content" : content
        }

    elif type == 'ceneje':
        data = {}
        data['category'] = re.compile(r"<div class=\"topContentBox\">[\s]+?<h1>(.*?)<\/h1>").search(page_content).group(1)
        data['numberOfListings'] = re.compile(r"<div class=\"numPro\">[\s]+?<b>(.*?)<\/b>").search(page_content).group(1)
        titles = re.compile(r"<div class=\"content\">[\s\S]*?<h3>[\s]*?<a onclick=\"GaTrackEvent.*?>(.*?)<\/a>").findall(page_content)
        prices = re.compile(r"<p class=\"priceInfo\">[\s\S]*?<a onclick=\"GaTrackEvent.*?>[\s\S]*?<b>(.*?)<\/b>").findall(page_content)
        stores = re.compile(r"<p class=\"priceInfo\">[\s\S]*?</a>[\s]*?<a href=.* class=\"qtySellers\">[\s]*?<b>\s*?(\w [\S| ]*)\s*?<\/b>").findall(page_content)
        k = 0
        for title in titles:
            data[title] = {
                'title': titles[k],
                'price': prices[k],
                'store': stores[k]
            }
            k += 1


    #print(data)
    return data



def saveToFile(fileName, data):
    with open(data_folder / fileName, 'w') as outfile:
        json.dump(data, outfile)

def process():

    rtvslo1 = open('input-extraction/Audi.html','r', encoding='utf8').read()
    # with open("text.txt", "w", encoding="utf8") as f:
    #     f.write(rtvslo1)
    rtvslo1_data = process_regex(rtvslo1,"rtvslo")
    saveToFile("Re-rtv1-output.json", rtvslo1_data)

    rtvslo2 = open('input-extraction/Volvo.html','r', encoding='utf8').read()
    rtvslo2_data = process_regex(rtvslo2,"rtvslo")
    saveToFile("Re-rtv2-output.json", rtvslo2_data)

    rac_novice1 = open('input-extraction/RacNovice1.html','r', encoding='utf8').read()
    rac_novice1_data = process_regex(rac_novice1,"rac_novice")
    saveToFile("Re-racNovice1-output.json", rac_novice1_data)

    overstock1 = open('input-extraction/jewelry01.html','r', encoding='utf-8', errors='ignore').read()
    doverstock1_data = process_regex(overstock1, "overstock")
    saveToFile("Re-overstock1-output.json", doverstock1_data)

    overstock2 = open('input-extraction/jewelry02.html','r', encoding='utf-8', errors='ignore').read()
    doverstock2_data = process_regex(overstock2, "overstock")
    saveToFile("Re-overstock2-output.json", doverstock2_data)

    ceneje1 = open('input-extraction/PC-Ceneje.si.html', 'r', encoding='utf-8', errors='ignore').read()
    ceneje1_data = process_regex(ceneje1, "ceneje")
    saveToFile("Re-ceneje1-output.json", ceneje1_data)

    ceneje2 = open('input-extraction/Kavci-Ceneje.si.html', 'r', encoding='utf-8', errors='ignore').read()
    ceneje2_data = process_regex(ceneje2, "ceneje")
    saveToFile("Re-ceneje2-output.json", ceneje2_data)





