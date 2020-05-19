from pathlib import Path
import sqlite3
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import nltk
import stopwords
from tqdm import tqdm
import sys

conn = sqlite3.connect('inverted-index.db')
data_folder = Path("input/")
dissalowed = ['', '-', '.', ',', '!', '?', '(', ')', '...', '--', ':', ';', '*', '×', '/', '@', '{', '}', '[', ']', '–',
              '©', '%', '$', '€', '``', "''", '....', '«', '»']


def create_db():
    c = conn.cursor()
    try:
        dropTableStatement = "DROP TABLE Posting"
        c.execute(dropTableStatement)
        dropTableStatement = "DROP TABLE IndexWord"
        c.execute(dropTableStatement)

        c.execute('''
                CREATE TABLE IndexWord (
                word TEXT PRIMARY KEY
            );
        ''')

        c.execute('''
            CREATE TABLE Posting (
                word TEXT NOT NULL,
                documentName TEXT NOT NULL,
                frequency INTEGER NOT NULL,
                indexes TEXT NOT NULL,
                snippets TEXT NOT NULL,
                PRIMARY KEY(word, documentName),
                FOREIGN KEY (word) REFERENCES IndexWord(word)
            );
        ''')

        print("Tabele so ustvarjene.")
    except:
        print("Povezava z bazo ni uspela.")

    conn.commit()


def insert_in_db(word, documentName, frequency, indexes, snippets):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO IndexWord (word) VALUES (?)", (word,))
    except:
        pass
    c.execute("INSERT INTO Posting (word,documentName,frequency,indexes,snippets) VALUES (?,?,?,?,?)",
              (str(word), str(documentName), frequency, indexes, snippets))

    conn.commit()


def insert_data(folder):
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
            stop_words = stopwords.stop_words_slovene
            text = nltk.word_tokenize(soup.get_text())
            text_lower = [x.lower() for x in text]
            filtered_sentence = [w for w in text_lower if not w in stop_words]
            result = {}
            index = 0
            for j in filtered_sentence:
                el = j.strip()
                el = ''.join([m for m in el if not m.isdigit()])
                if el not in dissalowed:
                    if el in result:
                        result[el].append(index)
                    else:
                        result[el] = [index]
                    index += 1

            for key in result:
                indexes = result[key]

                # Ustvarimo snippets
                snippet_indexes = [i for i, x in enumerate(text_lower) if x == key]
                snippets = []
                for snippet_i in snippet_indexes:
                    snippet = ""

                    num_words = 0
                    i_back = 1
                    # vzamemo 3 prejsnje besede, ne gremo dlje od 5 besed nazaj in pazimo da ne gremo out of bounds
                    while num_words < 3 and i_back <= 5 and snippet_i - i_back >= 0:
                        if text[snippet_i - i_back].isalnum():
                            num_words += 1
                        snippet = text[snippet_i - i_back] + " " + snippet
                        i_back += 1

                    snippet += text[snippet_i]

                    num_words = 0
                    i_forward = 1
                    while num_words < 3 and i_forward <= 5 and snippet_i + i_forward < len(text):
                        if text[snippet_i + i_forward].isalnum():
                            num_words += 1
                        snippet = snippet + " " + text[snippet_i + i_forward]
                        i_forward += 1

                    snippets.append(snippet)

                snippets_str = ' ... '.join(snippets)
                if not snippet_indexes == [] and snippet_indexes[0] > 4:
                    snippets_str = '... ' + snippets_str
                if not snippet_indexes == [] and snippet_indexes[len(snippet_indexes) - 1] < len(text) - 4:
                    snippets_str = snippets_str + '... '

                indexes = [str(x) for x in indexes]
                insert_in_db(key, str(folder) + '/' + str(i), len(indexes), ','.join(indexes), snippets_str)

    progress.close()


def main():
    print("Kreiranje tabel.")
    create_db()
    print("Začenjam vstavljanje podatkov iz e-prostor.gov.si")
    insert_data("e-prostor.gov.si")
    print("\nZačenjam vstavljanje podatkov iz e-uprava.gov.si")
    insert_data("e-uprava.gov.si")
    print("\nZačenjam vstavljanje podatkov iz evem.gov.si")
    insert_data("evem.gov.si")
    print("\nZačenjam vstavljanje podatkov iz podatki.gov.si")
    insert_data("podatki.gov.si")
    print("\nKončano!")


if __name__ == "__main__":
    main()
