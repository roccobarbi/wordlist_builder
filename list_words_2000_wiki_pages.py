import requests
from text_stripper import TextStripper
import time

time_start = int(time.time())
words = []
for i in range(2000):
    if i % 10 == 0:
        print(str(i))
    r = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/html")
    stripper = TextStripper(r.text)
    words.extend(stripper.strip_all().split())
low_words = []
for word in words:
    low_words.append(word.lower())
low_words = sorted(list(dict.fromkeys(low_words)))
time_end = int(time.time())
print(str(time_end - time_start))
index = 0
with open("out_2000_wiki.txt", "w") as outfile:
    for word in low_words:
        if index > 0:
            outfile.write("\n")
        outfile.write(word)
        index += 1
