import os, time, re, hashlib, json, requests, threading, queue
from logbook import Logger, StreamHandler, FileHandler
from itertools import islice

def get_current_event():
    with open('event_id.txt', 'r') as eventFile:
        return eventFile.read()


def set_current_event(event):
    with open('event_id.txt', 'w') as eventFile:
        eventFile.write(event)


def retrieve_events(file, numberOfEvents):
    with open(file) as f:
        return list(islice(f, numberOfEvents))


def get_hash(email, out_queue):
    hash = hashlib.md5()
    hash.update(email.encode('utf-8'))
    out_queue.put(hash.hexdigest())
    return hash.hexdigest()


def process_events(events):
    eventRegex = re.compile(r'eventId=(\d+)')
    emailRegex = re.compile(r'\bsuid=([A-Z0-9._%+-]+'
                            r'@[A-Z0-9.-]+'
                            r'\.'
                            r'[A-Z]{2,})\b',
                            flags=re.I | re.VERBOSE)
    eventList = []
    # For each event in the islice, try matching the regex
    for event in events:
        try:
            eventID, email =re.search(eventRegex, event).group(1), re.search(emailRegex, event).group(1)
            eventList.append([event, eventID, email])
        except Exception as e:
            print('Exception', e)
    return eventList


def create_threads(eventList):
    emailList = []
    for n in range(len(eventList)):
        emailList.append(eventList[n][2])
    # For each event in the list, create a thread which will get the hash with the email.
    out_queue = queue.Queue()
    x = 0
    jobs = list()
    while x < len(emailList):
        for y in range(5):
            jobs.append(threading.Thread(target=get_hash, args=(emailList[x], out_queue)))
            x += 1
        for job in jobs:
            job.start()
            job.join()
            print(out_queue.get())
        jobs.clear()


if __name__ == '__main__':
    start = time.time()
    file_path = r'C:\Users\stelam\PycharmProjects\EE_Tokenization\Logs\Test_dump2.log'
    events = retrieve_events(file_path, 20)
    eventList = process_events(events)
    create_threads(eventList)
    end = time.time()
    print(end-start)
