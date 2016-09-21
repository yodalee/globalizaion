#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import urllib2
import lxml.html
import time
import pickle


reload(sys)
sys.setdefaultencoding('utf-8')


TARGET = "http://doc.boyo.org.tw/gp/"


def getFun():
    request = urllib2.Request(TARGET)
    request.add_header("Pragma", "no-cache")
    response = urllib2.build_opener().open(request)

    content = response.read().decode('utf-8')
    root = lxml.html.fromstring(content)

    table = root.xpath("//table[@id='report']")[0]
    entries = table.xpath("//tr")
    question = []
    answer = []
    for q, a in zip(entries[1::2], entries[2::2]):
        if q[0].text is not None and a[0].text is not None:
            qtext = q[0].text.strip()
            atext = a[0].text.strip()
            question.append(qtext[3:].strip())
            answer.append(atext)

    return question, answer


def openPickle():
    try:
        return pickle.load(open("global", "rb"))
    except EOFError:
        return {}
    except IOError:
        return {}


def main():
    data = openPickle()
    hasNew = True
    count = 0
    maxCount = 10

    while True:
        time.sleep(1)
        hasNew = False
        newq, newa = getFun()

        for q, a in zip(newq, newa):
            if not data.has_key(q):
                hasNew = True
                data[q] = a
                print("%s %s" % (q, a))
        print("\n")

        if hasNew is True:
            count = 0
        else:
            count = count + 1

        pickle.dump(data, open("global", "wb"))

        if count == maxCount:
            break

    with open("globalization", "w") as f:
        for k, v in data.iteritems():
            f.write("%s\n%s\n" % (k, v))
    f.close()

if __name__ == "__main__":
    main()
