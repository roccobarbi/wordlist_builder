import requests
from text_stripper import TextStripper
import time

time_start = int(time.time())
words = []
download_time = 0
strip_time = 0
for i in range(200):
    if i % 10 == 0:
        print(str(i))
    download_start = time.time()
    r = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/html")
    download_time += time.time() - download_start
    strip_start = time.time()
    stripper = TextStripper(r.text)
    words.extend(stripper.strip_all().split())
    strip_time += time.time() - strip_start
low_words = []
for word in words:
    low_words.append(word.lower())
low_words = sorted(list(dict.fromkeys(low_words)))
time_end = int(time.time())
print("Total time: " + str(time_end - time_start))
print("Avg download: " + str(download_time/10000))
print("Avg strip: " + str(strip_time/10000))
index = 0
with open("out_200_wiki.txt", "w") as outfile:
    for word in low_words:
        if index > 0:
            outfile.write("\n")
        outfile.write(word)
        index += 1
