# Naloga 3
## Prerequisite
Note: code was developed in python version 3.6.2
1. In ./implementation-indexing directory run command `pip install -r requirements.txt`

## RUN database generator
1. In ./implementation-indexing directory run command `python run-data-process.py`

## RUN search
1. For BASIC search in ./implementation-indexing directory run command `python run-basic-search.py`
1. For SQLITE search in ./implementation-indexing directory run command `python run-sqlite-search.py`

# Naloga 2
## Prerequisite
Knjižnice:
1. from bs4 import Comment
2. from htmldom import htmldom
3. from lingpy import *
4. import re
5. from pathlib import Path
6. import sys
7. import json
9. from lxml import html
10. import regex
11. from pathlib import Path

## RUN extraction
Run one of the following commands (from the implementation-extraction directory), depending on the method you want to use:
1. Regular expression: *python .\run-extraction.py A*
2. XPath: *python .\run-extraction.py B*
3. RoadRunner: *python .\run-extraction.py C*

# Naloga 1

## Prerequisite
1. Add geckodriver.exe ro yur path
2. Run postgres  (host="localhost", port="5433", database="postgres", user="postgres", password="password")
3. Import database with script (https://szitnik.github.io/wier-labs/data/pa1/crawldb.sql)

## RUN crawler
1. In cmd run command: *python .\ieps.py*
2. Select how many threads you want to use
3. If you have ran it before you can choose to not delete the database and continue from where you left.

## Database dump file
https://filesender.arnes.si/?s=download&token=13f44407-2f24-488c-9223-eece91bbf6be&fbclid=IwAR1mGAOiLcNHYNfmPJ75k6uRHnnMVXLKGVFhK7-x8UxmOZrm2WVzvPyTN6E
