import requests
from text_stripper import TextStripper
import time
from multiprocessing import Process, Queue
import argparse


def download_pages(num, q, urls):
    for j in range(urls):
        r = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/html")
        q.put(r.text)
    print("Process: " + str(num) + " finished!")


def write_output(outfile_name):
    index = 0
    with open(outfile_name, "w") as outfile:
        for word in low_words:
            if index > 0:
                outfile.write("\n")
            outfile.write(word)
            index += 1


def define_advancement_unit(urls, processes):
    total_urls = urls * processes
    if total_urls < 100:
        advancement_unit = 1
    else:
        advancement_unit = int(total_urls / 100)
    return advancement_unit, total_urls


if __name__ == "__main__":
    time_start = int(time.time())
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-p", "--processes", type=int, default=1)
    argument_parser.add_argument("-u", "--urls", type=int, default=200)
    argument_parser.add_argument("-o", "--out", type=str, default=None)
    args = argument_parser.parse_args()
    if args.out is None:
        outfile_name = "out_" + str(args.processes) + "x" + str(args.urls) + "_wiki.txt"
    else:
        outfile_name = args.out
    advancement_unit, total_urls = define_advancement_unit(args.urls, args.processes)
    processes = []
    words = []
    queue = Queue()
    strip_counter = 0
    print("Spawning processes...")
    for i in range(args.processes):  # spawn the processes
        print(str(i))
        proc = Process(target=download_pages, args=(i, queue, args.urls))
        processes.append(proc)
        proc.start()
    print("Stripping...")
    try:
        while True:
            if strip_counter % advancement_unit == 0:
                print("Stripping URL: " + str(strip_counter) + " - " + str(int((strip_counter/total_urls)*100)) + "%")
            stripper = TextStripper(queue.get(block=True, timeout=2))
            words.extend(stripper.strip_all().split())
            strip_counter += 1
    except:
        print("Queue empty!")
    print("Closing processes...")
    for proc in processes:  # close the processes
        proc.join()
    low_words = []
    for word in words:
        low_words.append(word.lower())
    low_words = sorted(list(dict.fromkeys(low_words)))
    write_output(outfile_name)
    print("Total time: " + str(int(time.time()) - time_start))
