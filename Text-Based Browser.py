import requests
from bs4 import BeautifulSoup
from colorama import Fore

soup = BeautifulSoup(requests.get("https://docs.python.org").content, 'html.parser').find_all()
for i in soup:
    for ii in i:
        if ii.name == "a":
            ii.string = "".join([Fore.BLUE, ii.get_text(), Fore.RESET])
            
for i in soup:
   print(i.text) 
 
#for i in soup.find_all(("p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li")):
#    if i.a:
#        i.string = "".join([Fore.BLUE, i.get_text(), Fore.RESET])
#    print(i.text)