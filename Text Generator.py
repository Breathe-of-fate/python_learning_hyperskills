import nltk, random

with open(input(), "r", encoding="utf-8") as base:
    readed = base.read()

trigrams = list(nltk.ngrams(readed.split(), 3))
markov = dict()

for head, tail1, tail2 in trigrams:
    markov.setdefault(f"{head} {tail1}", {})
    markov[f"{head} {tail1}"].setdefault(tail2, 0)
    markov[f"{head} {tail1}"][tail2] += 1

for i in range(10):
    sentence = []
    while True:
        head = random.choice(list(markov))
        if head.split()[0].isalpha() and head.split()[0].istitle():
            break
        
    sentence += head.split()
    
    while True:
        choices = [i[0] for i in markov[head].items()]
        weights = [i[1] for i in markov[head].items()]
        next_word = random.choices(choices, weights, k=1)
        sentence += next_word
        head = f"{sentence[-2]} {next_word[0]}"
        if sentence[-1][-1] in ("?", ".", "!") and len(sentence) >= 5:
            break
    print(' '.join(sentence))