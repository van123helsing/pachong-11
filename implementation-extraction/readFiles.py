from pathlib import Path
from bs4 import BeautifulSoup


data_folder = Path("WebPages/")
overstock1 = data_folder / "Audi.html"
overstock2 = data_folder / "Volvo.html"
rtvslo1 = data_folder / "jewelry01.html"
rtvslo2 = data_folder / "jewelry02.html"
ceneje1 = data_folder / "PC-Ceneje.si.html"
ceneje2 = data_folder / "Kavci-Ceneje.si.html"
_24ur1 = data_folder / "24ur-1.html"
_24ur2 = data_folder / "24ur-2.html"

overstock1 = open(overstock1, "r")
overstock2 = open(overstock2, "r")
rtvslo1 = open(rtvslo1, "r")
rtvslo2 = open(rtvslo2, "r")
ceneje1 = open(ceneje1, "r")
ceneje2 = open(ceneje2, "r")
_24ur1 = open(_24ur1, "r")
_24ur2 = open(_24ur2, "r")

overstock1 = BeautifulSoup(overstock1.read(), 'html.parser')
overstock2 = BeautifulSoup(overstock2.read(), 'html.parser')
rtvslo1 = BeautifulSoup(rtvslo1.read(), 'html.parser')
rtvslo2 = BeautifulSoup(rtvslo2.read(), 'html.parser')
ceneje1 = BeautifulSoup(ceneje1.read(), 'html.parser')
ceneje2 = BeautifulSoup(ceneje2.read(), 'html.parser')
_24ur1 = BeautifulSoup(_24ur1.read(), 'html.parser')
_24ur2 = BeautifulSoup(_24ur2.read(), 'html.parser')
