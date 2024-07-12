import nltk, sys, math
from pysyllables import get_syllable_count

table = {"1": "5-6", "2": "6-7", "3": "7-8",
         "4": "8-9", "5": "9-10", "6": "10-11",
         "7": "11-12", "8": "12-13", "9": "13-14",
         "10": "14-15", "11": "15-16", "12": "16-17",
         "13": "17-18", "14": "18-22"}

with open(sys.argv[1], "r") as file:
    text = file.read()
    
with open(sys.argv[2], "r") as longman:
    longman3000 = longman.read().lower()
    longman3000 = sorted(longman3000.split())

chars = len([i for i in text if i not in " \n\t"])
sentences = len(nltk.tokenize.sent_tokenize(text))
words = nltk.tokenize.regexp_tokenize(text, r"[0-9A-z']+")
syllables = sum([1 if not get_syllable_count(i) else get_syllable_count(i) for i in words])
dif_words = len([i for i in words if i.lower() not in longman3000])

ari = 4.71 * (chars / len(words)) + 0.5 * (len(words) / sentences) - 21.43
fkrt = 0.39 * (len(words) / sentences) + 11.8 * (syllables / len(words)) - 15.59
dcri = 0.1579 * (dif_words / len(words)) * 100 + 0.0496 * (len(words) / sentences)
dcri = 3.6365 + dcri if dcri < 5 else dcri

rounded_ari = math.ceil(ari)
rounded_fkrt = math.ceil(fkrt)
rounded_drci = math.ceil(dcri)

print("Text:", text + "\n")
print("Characters:", chars)
print("Sentences:", sentences)
print("Words:", len(words))
print("Difficult words:", dif_words)
print("Syllables:", syllables)
print(f"\nAutomated Readability Index: {rounded_ari}. The text can be understood by {table[str(rounded_ari)]} year olds.")
print(f"Flesch–Kincaid Readability Test: {rounded_fkrt}. The text can be understood by {table[str(rounded_fkrt)]} year olds.")
print(f"Dale-Chall Readability Index: {rounded_drci}. The text can be understood by {table[str(rounded_drci)]} year olds.")

av_age = table[str(rounded_ari)].split("-") + table[str(rounded_fkrt)].split("-") + table[str(rounded_drci)].split("-")
av_age = [int(i) for i in av_age]
av_age = sum(av_age) / len(av_age)

print(f"\nThis text should be understood in average by {av_age} year olds.")