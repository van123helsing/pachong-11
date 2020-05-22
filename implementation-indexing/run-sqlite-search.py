import sqlite3
from tabulate import tabulate
import hashlib
import time

conn = sqlite3.connect('inverted-index.db')


def search(search_term):
    words = search_term.split(" ")

    output = {}
    for word in words:
        rows = select_from_db(word)
        for row in rows:
            key = hashlib.md5(row[1].encode()).hexdigest()
            if key not in output:
                output[key] = [row[0], row[1], row[2]]
            else:
                output[key][0] += row[0]
                output[key][2] += row[2]

    output = list(output.values())
    output.sort(key=lambda x: x[0], reverse=1)
    print(tabulate(output, headers=['Frequencies', 'Document', 'Snippet']))


def select_from_db(word):
    c = conn.cursor()
    try:
        c.execute("SELECT frequency, documentName, snippets FROM Posting WHERE word LIKE ?",
                  (word,))
    except:
        pass

    return c.fetchall()


def main():
    # search_term = "Sistem SPOT"
    # search_term = "predelovalne dejavnosti"
    # search_term = "trgovina"
    # search_term = "social services"
    # search_term = "ministrstvo za zdravje"
    # search_term = "republika slovenija"
    search_term = "računalništvo in informatika"
    print("Začenjam iskanje pojavitev: " + search_term)
    start_time = time.time()
    search(search_term)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("\nKončano!")


if __name__ == "__main__":
    main()
