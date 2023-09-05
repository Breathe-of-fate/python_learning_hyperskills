import string

alphabet = string.ascii_letters
key_length = int(input())
nonencoded_text = input().split()
encoded_text = input().split()
to_decode = input().split()
key_word = ""
word = ""

n = 0
while n != len(nonencoded_text):
  key_word += alphabet[(alphabet.index(encoded_text[n]) - alphabet.index(nonencoded_text[n]))]
  n += 1

end_key = key_word[:key_length]
n = 0
for i in to_decode:
  shift = (26 + alphabet.index(i) - alphabet.index(end_key[n])) % 26
  word += alphabet[shift]
  if n < len(end_key) - 1:
    n += 1
  else:
    n = 0

print(word.replace("x", " "))