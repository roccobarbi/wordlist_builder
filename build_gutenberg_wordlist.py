import requests

import text_stripper
from text_stripper import TextStripper
import time
from multiprocessing import Process, Queue
import argparse


def download_and_parse_books(num, q_in, q_out):
    while not q_in.empty():
        book = q_in.get()
        print("Requesting " + book)
        try:
            r = requests.get(book)
            print("Stripping " + book)
            s = text_stripper.TextStripper(r.text)
            print("Sending to queue " + book)
            q_out.put(s.strip_plaintext())
        except Exception as e:
            print("Could not load " + book)
            print(e.message)

    print("Process: " + str(num) + " finished!")


def write_output(outfile_name):
    index = 0
    with open(outfile_name, "w") as outfile:
        for word in low_words:
            if index > 0:
                outfile.write("\n")
            outfile.write(word)
            index += 1


if __name__ == "__main__":
    time_start = int(time.time())
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-p", "--processes", type=int, default=1, help="Number of max processes (default 1).")
    argument_parser.add_argument("-o", "--out", type=str, default=None, help="Optional name of the output file.")
    argument_parser.add_argument("-m", "--merge", type=str, default=None, help="Optional name of a partial list to merge with the new one.")
    args = argument_parser.parse_args()
    if args.out is None:
        outfile_name = "out_gutenberg_" + str(int(time.time())) + ".txt"
    else:
        outfile_name = args.out
    books = [
        "https://gutenberg.org/files/84/84-0.txt",
        "https://gutenberg.org/files/1342/1342-0.txt",
        "https://gutenberg.org/cache/epub/25344/pg25344.txt",
        "https://gutenberg.org/files/1661/1661-0.txt",
        "https://gutenberg.org/files/844/844-0.txt",
        "https://gutenberg.org/cache/epub/67195/pg67195.txt",
        "https://gutenberg.org/files/11/11-0.txt",
        "https://gutenberg.org/cache/epub/67191/pg67191.txt",
        "https://gutenberg.org/files/2542/2542-0.txt",
        "https://gutenberg.org/files/1080/1080-0.txt",
        "https://gutenberg.org/files/98/98-0.txt",
        "https://gutenberg.org/cache/epub/64317/pg64317.txt",
        "https://gutenberg.org/files/2701/2701-0.txt",
        "https://gutenberg.org/files/1952/1952-0.txt",
        "https://gutenberg.org/cache/epub/46/pg46.txt",
        "https://gutenberg.org/cache/epub/67190/pg67190.txt",
        "https://gutenberg.org/files/4300/4300-0.txt",
        "https://gutenberg.org/files/174/174-0.txt",
        "https://gutenberg.org/files/345/345-0.txt",
        "https://gutenberg.org/files/5200/5200-0.txt",
        "https://gutenberg.org/files/219/219-0.txt",
        "https://gutenberg.org/files/408/408-0.txt",
        "https://gutenberg.org/files/76/76-0.txt",
        "https://gutenberg.org/files/2591/2591-0.txt",
        "https://gutenberg.org/ebooks/514.txt.utf-8",
        "https://gutenberg.org/files/35/35-0.txt"
    ]
    processes = []
    words = []
    if args.merge is not None:
        with open(args.merge, "r") as infile:
            for line in infile:
                words.append(line.strip())
    books_queue = Queue()
    words_queue = Queue()
    print("Queueing books...")
    for book in books:
        books_queue.put(book)
    print("Spawning downloaders...")
    for i in range(args.processes):  # spawn the processes
        proc = Process(target=download_and_parse_books, args=(i, books_queue, words_queue))
        processes.append(proc)
        proc.start()
    print("Merging the words...")
    try:
        while True:
            print(".")
            words.extend(words_queue.get(block=True, timeout=20).split())
    except:
        print("Queue empty!")
    print("Closing downloaders...")
    for proc in processes:  # close the processes
        proc.join()
    print("Writing results...")
    low_words = []
    for word in words:
        low_words.append(word.lower())
    low_words = sorted(list(dict.fromkeys(low_words)))
    write_output(outfile_name)
    print("Total time: " + str(int(time.time()) - time_start))
