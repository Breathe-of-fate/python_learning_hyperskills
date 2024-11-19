import requests, sys
from bs4 import BeautifulSoup

name, start_language, finish_language, what = sys.argv

languages = ["arabic", "german", "english", "spanish", "french", "hebrew", 
             "japanese", "dutch", "polish", "portuguese", "romanian", "russian", "turkish"]

fin_language = languages if finish_language == "all" else [finish_language]

to_output = ""

for i in fin_language:
    responce = requests.get(f'https://context.reverso.net/translation/{start_language.lower()}-{i.lower()}/{what}', 
                            headers={'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'})
    checked = start_language if start_language not in languages else finish_language if finish_language not in languages else True
    if checked and finish_language != "all":
        print(f"Sorry, the program doesn't support {checked}")
        sys.exit()
    elif responce.status_code == 404:
        print(f"Sorry, unable to find {what}")
        sys.exit()
    elif 400 < responce.status_code <= 599:
        print("Something wrong with your internet connection")
        sys.exit()
    content = BeautifulSoup(responce.content, 'html.parser')
    words = [i.text for i in content.find_all("span", {"class": "display-term"})]
    target_sentenses = [i.text.strip("\n\r ") for i in content.find_all("div", {"class": ["src ltr", "trg rtl arabic", "trg rtl"]})]
    second_sentenses = [i.text.strip("\n\r ") for i in content.find_all("div", {"class": ["trg ltr", "trg rtl arabic", "trg rtl"]})]
    all_senteses = ["\n".join(i) for i in zip(target_sentenses, second_sentenses)]
    to_output += f"{i.capitalize()} Translations:\n" + "\n".join(words) + "\n\n" + f"{i.capitalize()} Examples:\n" + "\n".join(all_senteses) + "\n\n"

print(to_output)

with open(f"{what}.txt", "a+", encoding="utf-8") as file: file.write(to_output)