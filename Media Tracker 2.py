import requests
import re
import bs4
import urllib
import time
import pandas as pd
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}

start_date = '6/2/2022'
end_date = '7/19/2022'

search_string = ["Center for Community Alternatives", "Communities Not Cages New York",
                 "Marvin Mayfield", "Katie Schaffer", "Nyatwa Bullock",
                "Clean Slate New York","Bail Reform New York","Parole Reform New York",
                "Elder Parole New York", "Second Look Act New York", "Earned Time Act New York",
                "Eliminate Mandatory Minimums New York", "Judicial Accountability Act New York"]

"""
# Entire Word Bank
word_bank = ["Center for Community Alternatives", "Nyatwa Bullock",
                 "Garrett Smith", "Marvin Mayfield", "Katie Schaffer",
                 "Communities Not Cages", "Myrie", "Latrice Walker"
                 "Discovery Reform", "bail rollback", "Bail rollback", 
                 "Bail Rollback", "bail reform", "Bail reform", 
                 "Bail Reform" "Elder Parole", "elder parole",
                 "Pete Martin", "Peter Martin","judicial accountability",
                 "Judicial Accountability", "Mandatory Minimums",
                 "mandatory minimums", "center for community alternatives",
                 "communities not cages", "parole justice",
                 "Parole Justice", "parole reform", "Parole Reform"]
"""

# CCA + Employees Word Bank
word_bank = ["Center for Community Alternatives", "Nyatwa Bullock",
                 "Garrett Smith", "Marvin Mayfield", "Katie Schaffer",
                 "Pete Martin", "Peter Martin", "center for community alternatives",
                 "Tammar Cancer"]


"""
# Bills Word Bank
word_bank = ["Discovery Reform", "bail reform", "Bail reform", 
                 "Bail Reform" "Elder Parole", "elder parole",
                 "judicial accountability", "Judicial Accountability", 
                 "Mandatory Minimums", "mandatory minimums",
                 "communities not cages", "parole justice",
                 "Parole Justice", "parole reform", "Parole Reform",
                 "Communities Not Cages"]
"""

page_list = ['0','10','20','30','40','50']

finished_list = []
for search in search_string: 
    for page in page_list:
        url = 'https://www.google.com/search?q=' + search + '&tbs=cdr:1,cd_min:' + start_date + ',cd_max:' + end_date + '&tbm=nws&start=' + page
        reqs = requests.get(url, headers = headers)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        done_list = []
        for link in soup.find_all('a',href=re.compile("https")):
                done_list.append(link.get('href'))
        finished_list += (done_list)
        time.sleep(0.6)
    
finished_list = list(set(finished_list))


empty3 = []
non_used_links = []

for link in finished_list:
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req)
        soup = bs(page, 'html.parser')

        empty2 = []
        for x in word_bank:
            if x in soup.text.strip():
                y = True
            else:
                y = False
            empty2.append(y)
        empty2

        if any(x == True for x in empty2):
            empty3.append(link)
            print(link)
        else:
            non_used_links.append(link)
    except: 
        continue
        
empty4 = []

for link in empty3:

    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    # using the BeautifulSoup module
    soup = BeautifulSoup(urlopen(req))

    # displaying the title
    empty4.append(soup.title.get_text())

empty5 = []

from htmldate import find_date

for link in empty3: 
    try: 
        empty5.append(find_date(link))
    except: 
        empty5.append("None Found")
        
empty6 = []

for link in empty3:
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    soup = bs(page, 'html.parser')

    string = ''

    for x in word_bank:
        if x in soup.text.strip():
            string += x
            string += ', '
        else:
            continue
    empty6.append(string[:-2])
    

    
df = pd.DataFrame({'Date': empty5, 'Article': empty4, 'Key Words': empty6,'Link': empty3})
print(df)
