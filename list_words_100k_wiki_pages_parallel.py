import requests
from text_stripper import TextStripper
import time
from multiprocessing import Process, Queue


def download_pages(num, q, urls):
    for j in range(urls):
        r = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/html")
        q.put(r.text)
    print("Process: " + str(num) + " finished!")

if __name__ == "__main__":
    time_start = int(time.time())
    processes = []
    words = []
    queue = Queue()
    number_of_processes = 20
    urls_per_process = 5000
    strip_counter = 0
    print("Spawning processes...")
    for i in range(number_of_processes):  # spawn the processes
        print(str(i))
        proc = Process(target=download_pages, args=(i, queue, urls_per_process))
        processes.append(proc)
        proc.start()
    print("Processes: " + str(len(processes)))
    print("Stripping...")
    try:
        while True:
            if strip_counter % 10 == 0:
                print("Stripping URL: " + str(strip_counter))
            strip_start = time.time()
            stripper = TextStripper(queue.get(block=True, timeout=2))
            words.extend(stripper.strip_all().split())
            strip_counter += 1
    except:
        print("Queue empty!")
    print("Closing processes...")
    print("Current processes: " + str(len(processes)))
    for proc in processes:  # close the processes
        proc.join()
    low_words = []
    for word in words:
        low_words.append(word.lower())
    low_words = sorted(list(dict.fromkeys(low_words)))
    time_end = int(time.time())
    print("Total time: " + str(time_end - time_start))
    index = 0
    with open("out_100k_wiki.txt", "w") as outfile:
        for word in low_words:
            if index > 0:
                outfile.write("\n")
            outfile.write(word)
            index += 1
