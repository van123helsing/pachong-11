from pathlib import Path
import sqlite3
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import nltk
import stopwords
from tqdm import tqdm
from tabulate import tabulate
import sys
import time

data_folder = Path("input/")
dissalowed = ['', '-', '.', ',', '!', '?', '(', ')', '...', '--', ':', ';', '*', '×', '@', '{', '}', '[', ']', '–',
              '©', '%', '$', '€', '``', "''", '....', '«', '»']

frequencies = {}
snippet = {}
stop_words = stopwords.stop_words_slovene


def match(text, words, file):
    words = words.split(" ")
    for i in range(len(text)):
        counter = 0
        trigger_a = True
        trigger_b = True
        words_s = ""
        for j in range(len(words)):
            if i + j < len(text) and words[j].lower() == text[i + j].lower() and words[j] not in stop_words:
                words_s = words_s + " " + text[i + j]
                counter += 1

        j = len(words)
        if counter > 0:
            okol_a = ""
            okol_b = ""
            for k in range(0, 3):
                if i + j + k < len(text):
                    okol_b = okol_b + " " + text[i + j + k]
                if i - k - 1 >= 0:
                    okol_a = text[i - k - 1] + " " + okol_a

            snip = okol_a + words_s + okol_b

            if file in frequencies:
                frequencies[file] += 1
                snippet[file].append(snip)
            else:
                frequencies[file] = 1
                snippet[file] = [snip]


def search(folder, words):
    folder = data_folder / folder
    files = [f for f in listdir(folder) if isfile(join(folder, f))]

    progress = tqdm(files, file=sys.stdout)
    for i in progress:
        if i.endswith('html'):
            file = folder / i
            f = open(file, "r", encoding='utf-8', errors='ignore')
            soup = BeautifulSoup(f.read(), 'html.parser')
            for s in soup.select('script'):
                s.extract()
            for s in soup.select('style'):
                s.extract()

            text = nltk.word_tokenize(soup.get_text())
            match(text, words, file)

    progress.close()


if __name__ == "__main__":
    # words = "Sistem SPOT"
    # words = "predelovalne dejavnosti"
    # words = "trgovina"
    # words = "social services"
    # words = "ministrstvo za zdravje"
    # words = "republika slovenija"
    words = "računalništvo in informatika"

    start_time = time.time()

    files = [f for f in listdir(data_folder)]
    for i in files:
        search(i, words)

    sorted_freq = {k: v for k, v in sorted(frequencies.items(), key=lambda item: item[1], reverse=True)}
    table = []
    for i in sorted_freq:
        row = []
        row.append(sorted_freq.get(i))
        row.append(i)
        row.append("..." + "...".join(snippet[i]))
        table.append(row)

    print(tabulate(table, headers=['Frequencies', 'Document', 'Snippet']))
    print("--- %s seconds ---" % (time.time() - start_time))

    # for i in frequencies:
    #     print(str(i).replace("input\\",""))
    # print(str(list(frequencies.keys())[0]).replace("input\\",""))
