import readFiles
from bs4 import Comment


def clean(body):
    # izberemo samo body element
    body = body.find('body')
    # izbrisemo vse script elemente
    for s in body.select('script'):
        s.extract()
    # izbrisemo vse style elemente
    for s in body.select('style'):
        s.extract()
    # izbrisemo vse komentarje
    for s in body(text=lambda text: isinstance(text, Comment)):
        s.extract()

    return body

def compare(h1, h2):
    return


body1 = clean(readFiles.overstock1)
body2 = clean(readFiles.overstock2)
