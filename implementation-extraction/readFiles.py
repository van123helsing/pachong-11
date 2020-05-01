from pathlib import Path
from bs4 import BeautifulSoup

data_folder = Path("input-extraction/")
overstock1 = data_folder / "jewelry01.html"
overstock2 = data_folder / "jewelry02.html"
rtvslo1 = data_folder / "Audi.html"
rtvslo2 = data_folder / "Volvo.html"
ceneje1 = data_folder / "PC-Ceneje.si.html"
ceneje2 = data_folder / "Kavci-Ceneje.si.html"
RacNovice1 = data_folder / "RacNovice1.html"
RacNovice2 = data_folder / "RacNovice2.html"

overstock1 = open(overstock1, "r", encoding='utf-8', errors='ignore')
overstock2 = open(overstock2, "r", encoding='utf-8', errors='ignore')
rtvslo1 = open(rtvslo1, "r", encoding='utf-8', errors='ignore')
rtvslo2 = open(rtvslo2, "r", encoding='utf-8', errors='ignore')
ceneje1 = open(ceneje1, "r", encoding='utf-8', errors='ignore')
ceneje2 = open(ceneje2, "r", encoding='utf-8', errors='ignore')
RacNovice1 = open(RacNovice1, "r", encoding='utf-8', errors='ignore')
RacNovice2 = open(RacNovice2, "r", encoding='utf-8', errors='ignore')

overstock1 = BeautifulSoup(overstock1.read(), 'html.parser')
overstock2 = BeautifulSoup(overstock2.read(), 'html.parser')
rtvslo1 = BeautifulSoup(rtvslo1.read(), 'html.parser')
rtvslo2 = BeautifulSoup(rtvslo2.read(), 'html.parser')
ceneje1 = BeautifulSoup(ceneje1.read(), 'html.parser')
ceneje2 = BeautifulSoup(ceneje2.read(), 'html.parser')
RacNovice1 = BeautifulSoup(RacNovice1.read(), 'html.parser')
RacNovice2 = BeautifulSoup(RacNovice2.read(), 'html.parser')
