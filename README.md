# Naloga 2
## Prerequisite
Knjižnice:
1. from bs4 import Comment
2. from htmldom import htmldom
3. from lingpy import *
4. import re
5. from pathlib import Path
6. import sys

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
