import readFiles
from bs4 import Comment
from htmldom import htmldom
from lingpy import *
import re
from pathlib import Path

data_folder = Path("input-extraction/output/RoadRunner/")


def clean(body):
    # izberemo samo body element
    body = body.find('body')
    # izbrisemo vse script elemente
    for s in body.select('script'):
        s.extract()
    # izbrisemo vse style elemente
    for s in body.select('style'):
        s.extract()
    # izbrisemo vse iframe elemente
    for s in body.select('iframe'):
        s.extract()
    # izbrisemo vse komentarje
    # for s in body(text=lambda text: isinstance(text, Comment)):
    # s.extract()
    # izbrisemo vse nepotrebne atribute
    for p in body.findAll(True):
        if 'style' in p.attrs:
            del p.attrs['style']
        if 'id' in p.attrs:
            del p.attrs['id']
        if 'class' in p.attrs:
            del p.attrs['class']
        if 'target' in p.attrs:
            del p.attrs['target']
        if 'rel' in p.attrs:
            del p.attrs['rel']
        if 'type' in p.attrs:
            del p.attrs['type']
        if 'onclick' in p.attrs:
            del p.attrs['onclick']
        if 'role' in p.attrs:
            del p.attrs['role']
        if 'tabindex' in p.attrs:
            del p.attrs['tabindex']
        if 'action' in p.attrs:
            del p.attrs['action']
        if 'method' in p.attrs:
            del p.attrs['method']

    # izbrisemo prazne elemente
    [x.decompose() for x in body.findAll(lambda tag: (not tag.contents or len(
        tag.get_text(strip=True)) <= 0) and not tag.name == 'a')]

    return body


def DOMtoArray(node, array):
    for j in node.children:
        if j.nodeName != 'text':
            if j.nodeName == 'a' and 'href' in j.attributes:
                array.append('<a href=' + j.attributes.get('href')[0] + '>')
            else:
                array.append('<' + j.nodeName + '>')
            DOMtoArray(j, array)
            array.append('</' + j.nodeName + '>')
        else:
            array.append('/text/' + j.text)


def compare(h1, h2, isShort):
    result = ["<body>"]
    dom1 = htmldom.HtmlDom()
    dom2 = htmldom.HtmlDom()
    dif1 = dom1.createDom(h1)
    dif2 = dom2.createDom(h2)

    array1 = []
    node = dif1.referenceToRootElement
    DOMtoArray(node, array1)

    array2 = []
    node = dif2.referenceToRootElement
    DOMtoArray(node, array2)

    almA, almB, sim = nw_align(array1, array2)

    roadRunner(almA, almB, result, isShort)

    for n in range(len(result)):
        result[n] = re.sub("<a\shref=.+?>", '<a href=...>', result[n])

    result.append("</body>")

    return result


def roadRunner(array1, array2, result, isShort):
    align_len = len(array1)
    i = 0
    while i < align_len:
        if array1[i].startswith('/text/'):
            if not array1[i] == array2[i]:
                izpisiPrviTag(array1, array2, i, result)
            else:
                izpisiPrviTag(array1, array2, i, result)

        elif not array1[i].startswith('</') and not array1[i].startswith('/text/'):

            if array1[i] == '-':
                poddrevo = sestaviPoddrevo(align_len, array2, i)
            else:
                poddrevo = sestaviPoddrevo(align_len, array1, i)

            if not array1[i:poddrevo + 1] == array2[i:poddrevo + 1]:

                if onlyMinus(array1[i:poddrevo + 1]):
                    if array2[i] != '<div>' and (
                            (result[len(result) - 1].replace('</', '<', 1)).startswith((array2[i].split(' ')[0])) or (
                    result[len(result) - 1].replace('(<', '<', 1)).startswith((array2[i].split(' ')[0]))):
                        result.append('(' + ''.join(array2[i:poddrevo + 1]) + ')+ ')
                    else:
                        result.append('(' + ''.join(array2[i:poddrevo + 1]) + ')? ')
                    i = poddrevo
                elif onlyMinus(array2[i:poddrevo + 1]):
                    if array1[i] != '<div>' and (
                            (result[len(result) - 1].replace('</', '<', 1)).startswith((array1[i].split(' ')[0])) or (
                    result[len(result) - 1].replace('(<', '<', 1)).startswith((array1[i].split(' ')[0]))):
                        result.append('(' + ''.join(array1[i:poddrevo + 1]) + ')+ ')
                    else:
                        result.append('(' + ''.join(array1[i:poddrevo + 1]) + ')? ')

                    i = poddrevo
                else:
                    if not isShort:
                        izpisiPrviTag(array1, array2, i, result)

                    if poddrevo - i > 1:
                        roadRunner(array1[i + 1:poddrevo], array2[i + 1:poddrevo], result, isShort)
                        i = poddrevo

                    if not isShort:
                        izpisiZadnjiTag(array1, array2, poddrevo, result)
            else:
                i = poddrevo
        i += 1


def izpisiZadnjiTag(array1, array2, poddrevo, result):
    if array1[poddrevo] == '-':
        if not array2[poddrevo].startswith('/text/'):
            result.append(array2[poddrevo])
    else:
        if not array1[poddrevo].startswith('/text/'):
            result.append(array1[poddrevo])


def izpisiPrviTag(array1, array2, i, result):
    if array1[i] == '-':
        if array2[i].startswith('/text/'):
            result.append('#text')
        else:
            result.append(array2[i])
    else:
        if array1[i].startswith('/text/'):
            if array2[i] == array1[i]:
                result.append(array1[i])
            else:
                result.append('#text')
        else:
            result.append(array1[i])


def sestaviPoddrevo(ln, array1, i):
    count = 0
    for j in range(i + 1, ln, 1):
        if not array1[j].startswith('/text/') and array1[j].startswith('</' + (array1[i].split(' ')[0])[1:]):
            if count == 0:
                return j
            else:
                count = count - 1
        elif array1[i] == array1[j]:
            count += 1
    return ln - 1


def onlyMinus(array):
    for c in array:
        if c != '-':
            return False
    return True


def saveToFile(fileName, array):
    file1 = open(data_folder / fileName, "w", errors='ignore')
    for i in array:
        file1.write(i)
    file1.close()


def process():
    print("STARTED COMPARING RTVSLO")
    body1 = clean(readFiles.rtvslo1)
    body2 = clean(readFiles.rtvslo2)
    res_short = compare(str(body1), str(body2), True)
    res_full = compare(str(body1), str(body2), False)

    print("STARTED COMPARING OVERSTOCK")
    body1 = clean(readFiles.overstock1)
    body2 = clean(readFiles.overstock2)
    res2_short = compare(str(body1), str(body2), True)
    res2_full = compare(str(body1), str(body2), False)

    print("STARTED COMPARING CENEJE.SI")
    body1 = clean(readFiles.ceneje1)
    body2 = clean(readFiles.ceneje2)
    res3_short = compare(str(body1), str(body2), True)
    res3_full = compare(str(body1), str(body2), False)

    print("STARTED COMPARING RačunalniškeNovice")
    body1 = clean(readFiles.RacNovice1)
    body2 = clean(readFiles.RacNovice2)
    res4_short = compare(str(body1), str(body2), True)
    res4_full = compare(str(body1), str(body2), False)
    print("DONE")

    saveToFile("rtvslo-output-short.html", res_short)
    saveToFile("overstock-output-short.html", res2_short)
    saveToFile("ceneje-output-short.html", res3_short)
    saveToFile("racNovice-output-short.html", res4_short)
    saveToFile("rtvslo-output-full.html", res_full)
    saveToFile("overstock-output-full.html", res2_full)
    saveToFile("ceneje-output-full.html", res3_full)
    saveToFile("racNovice-output-full.html", res4_full)
    print("ALL FILES SAVED TO ./input-extraction/output/RoadRunner/ DIRECTORY.")

