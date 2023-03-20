import requests
from bs4 import BeautifulSoup
import string
import os

pages = [str(i) for i in range(1, int(input()) + 1)]
a_type = input()

for page_num in pages:
    r = requests.get('https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=' + page_num)
    soup = BeautifulSoup(r.content, 'html.parser')
    news_cards = soup.findAll('span', {'class': 'c-meta__type'}, text=a_type)
    news_links = ["https://www.nature.com" + i.find_parent('article').find('a').get('href') for i in news_cards]
    news_titles = [i.find_parent('article').find('a').text.strip(string.punctuation).replace(" ", "_") for i in news_cards]
    links_content = [BeautifulSoup(requests.get(i).content, 'html.parser').find('p', {'class': 'article__teaser'}).text for i in news_links]
    os.mkdir('Page_' + page_num) if not os.path.isdir(f'Page_{page_num}') else None
    for i in news_titles:
        for ii in links_content:
            with open(f"Page_{page_num}\{i}.txt", 'w', encoding="UTF-8") as output:
                output.write(ii)