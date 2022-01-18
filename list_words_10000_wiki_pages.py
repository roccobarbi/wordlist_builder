import requests
from text_stripper import TextStripper
import time

time_start = int(time.time())
words = []
download_time = 0
strip_time = 0
for i in range(10000):
    if i % 10 == 0:
        print(str(i))
    download_start = time.time()
    r = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/html")
    download_time += time.time() - download_start
    strip_start = time.time()
    stripper = TextStripper(r.text)
    words.extend(stripper.strip_all().split())
    strip_time += strip_start - time.time()
low_words = []
for word in words:
    low_words.append(word.lower())
low_words = sorted(list(dict.fromkeys(low_words)))
time_end = int(time.time())
print("Total time: " + str(time_end - time_start))
print("Avg download: " + str(int(download_time/10000)))
print("Avg strip: " + str(int(strip_time/10000)))
index = 0
with open("out_10000_wiki.txt", "w") as outfile:
    for word in low_words:
        if index > 0:
            outfile.write("\n")
        outfile.write(word)
        index += 1
