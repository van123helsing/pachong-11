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
              '©', '%', '$', '€','``', "''",'....' ,'«','»' ]


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
                PRIMARY KEY(word, documentName),
                FOREIGN KEY (word) REFERENCES IndexWord(word)
            );
        ''')
        print("Tabele so ustvarjene.")
    except:
        print("Povezava z bazo ni uspela.")

    conn.commit()


def insert_in_db(word, documentName, frequency, indexes):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO IndexWord (word) VALUES (?)", (word,))
    except:
        pass
    c.execute("INSERT INTO Posting (word,documentName,frequency,indexes) VALUES (?,?,?,?)", (str(word),str(documentName),frequency,indexes))

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
            text = [x.lower() for x in text]
            filtered_sentence = [w for w in text if not w in stop_words]
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
                value = result[key]
                value = [str(x) for x in value]
                insert_in_db(key, str(folder)+'/'+str(i), len(value), ','.join(value))

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
