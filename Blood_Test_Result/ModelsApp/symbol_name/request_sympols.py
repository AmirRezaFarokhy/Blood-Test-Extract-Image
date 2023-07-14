import requests 
from bs4 import BeautifulSoup
import csv

urls = "https://www.laboratoryalliance.com/healthcare-providers/laboratory-services/test-abbreviations/"
get = requests.get(urls)
soup = BeautifulSoup(get.text, 'html.parser')
dives_class = soup.findAll("div", {"class":"WordSection1"})

def Symbols(dives):
    sym = {}
    for div in dives:
        rows = div.findAll('tr')
        for row in rows:
            tds = str(row.findAll("td"))
            td = tds.replace("<td>", " ").replace("</td>", " ")[1:-1].split(",")
            if len(td[0])<10:
                sym[td[1].strip()] = td[0].strip()
    return sym

dataset = Symbols(dives_class)
with open("symbols.csv", "w") as files:
    f = csv.writer(files)
    for key, val in dataset.items():
        f.writerow([key, val])

