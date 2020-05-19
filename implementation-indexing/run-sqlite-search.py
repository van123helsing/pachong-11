import sqlite3
from tabulate import tabulate
import hashlib


conn = sqlite3.connect('inverted-index.db')


def search(search_term):
    words = search_term.split(" ")

    output = {}
    for word in words:
        rows = select_from_db(word)
        for row in rows:
            key = hashlib.md5(row[1].encode()).hexdigest()
            if key not in output:
                output[key] = [row[0], row[1], get_snippet(row[2])]
            else:
                output[key][0] += row[0]
                output[key][2] += ' ... ' + get_snippet(row[2])

    output = list(output.values())
    output.sort(key=lambda x: x[0], reverse=1)
    print(tabulate(output, headers=['Frequencies', 'Document', 'Snippet']))


def select_from_db(word):
    c = conn.cursor()
    try:
        c.execute("SELECT frequency, documentName, Indexes FROM Posting WHERE word LIKE ?",
                  (word,))
    except:
        pass

    return c.fetchall()


def get_snippet(word, document, index):
    c = conn.cursor()
    try:
        c.execute("SELECT frequency, documentName, word FROM Posting WHERE word LIKE ?",
                  (word,))
    except:
        pass

    return c.fetchall()


def main():
    search_term = "Sistem SPOT"
    print("Začenjam iskanje pojavitev: " + search_term)
    search(search_term)
    print("\nKončano!")


if __name__ == "__main__":
    main()
