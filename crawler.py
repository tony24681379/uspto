import math
import re

import requests
from bs4 import BeautifulSoup

headers = {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }

def parse_search_page(url):
    prefix = 'https://patft.uspto.gov'
    html = requests.get(prefix+url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    num = soup.find_all('table')[2].find_all('b')[1].string.strip()
    date = soup.find_all('table')[2].find_all('b')[3].string.strip()
    title = soup.find_all('font')[3].string.strip()
    abstract = soup.find_all('p')[0].get_text(strip=True).replace('\n', '').replace('  ', '')

    target = soup.find_all('p')[1]
    claim = BeautifulSoup(str(target)[str(target).index('<center><b><i>Claims</i></b></center>')+38:str(target).index('<center><b><i>Description</i></b></center>')]).get_text().replace('\n', ' ')
    description = BeautifulSoup(str(target)[str(target).index('<center><b><i>Description</i></b></center>')+43:str(target).index('<center><b>* * * * *</b></center>')]).get_text().replace('\n', ' ')

    international_class = soup.find_all('table')[7].find_all('td')[3].get_text().replace('\xa0', ' ')
    filed_date = soup.find_all('td', align='left',width='90%')[-1].get_text().replace('\n', '')
    assignee = soup.find_all('td', align='left',width='90%')[2].get_text().replace('\n', '')

def main():
    term='("stylus+pen"+OR+"electronic+stylus")+AND+coil'
    page = 1
    url = 'https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p='+str(page)+'&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&f=S&l=50&d=PTXT&Query='+term

    html = requests.get(url, headers=headers)

    soup = BeautifulSoup(html.text, 'html.parser')
    total = int(soup.find_all('strong')[2].string)
    total_page = math.ceil(total / 50)
    print(total_page)

    for page in range(1, total_page):
        url = 'https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p='+str(page)+'&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&f=S&l=50&d=PTXT&Query='+term
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        table = soup.find_all('table')[1]
        links = table.find_all(href=re.compile("/netacgi/nph-Parser\?Sect1=PTO2&Sect2="))
        i = 0
        add = []
        print('page:' + str(page))
        for row in links:
            i += 1
            if i % 2 == 0:
                add.append(row.attrs.get('href'))
                print('row: ' + str(row.attrs.get('href')))

if __name__ == "__main__":
    main()
