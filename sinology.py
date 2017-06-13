#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib.request
import lxml.html
import time
import pickle


TARGET = "http://doc.boyo.org.tw/sinology/"
picklefile = "sinology.pickle"


def getFun():
    req = urllib.request.Request(TARGET)
    req.add_header("Pragma", "no-cache")
    response = urllib.request.build_opener().open(req)

    content = response.read().decode('utf-8')
    root = lxml.html.fromstring(content)

    table = root.xpath("//table[@id='report']")[0]
    entries = table.xpath("//tr")
    question = []
    answer = []
    for q, a in zip(entries[1::2], entries[2::2]):
        if q[0].text is not None and a[0].text is not None:
            qtext = q[0].text_content().replace('\r', '').strip()
            atext = a[0].text_content().replace('\r', '').strip()
            question.append(qtext[3:].strip())
            answer.append(atext)

    return question, answer


def openPickle():
    try:
        return pickle.load(open(picklefile, "rb"))
    except (EOFError, IOError):
        return {}


def main():
    data = openPickle()
    hasNew = True
    count = 0
    maxCount = 20

    while True:
        time.sleep(0.5)
        hasNew = False
        newq, newa = getFun()

        # store new data
        for q, a in zip(newq, newa):
            if not q in data:
                hasNew = True
                data[q] = a
                print("%s %s" % (q, a))
        print("\n")

        # dump to pickle
        pickle.dump(data, open(picklefile, "wb"))

        # terminate condition
        if hasNew is True:
            count = 0
        else:
            count = count + 1

        if count == maxCount:
            break

    with open("sinology", "w") as f:
        for k, v in data.items():
            f.write("Q: %s\nA: %s\n" % (k, v))
    f.close()

if __name__ == "__main__":
    main()
