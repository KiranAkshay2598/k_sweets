import re
import fileinput, codecs
from bs4 import BeautifulSoup

f = codecs.open('templates/index.html', 'r', 'utf-8')
document = BeautifulSoup(f.read())
links = document.find_all('a',href=True)
print(links[0])