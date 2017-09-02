#!/usr/bin/python
import textract
import sys
from pycorenlp import StanfordCoreNLP

reload(sys)
sys.setdefaultencoding("utf-8")

def pdfToText(pathToPdf):
    nlp = StanfordCoreNLP("http://localhost:9000")
    text = textract.process(pathToPdf)

    start = text.find("In the second quarter of the year")
    end = text.find("\n\n",start)

    with open("wholeDocument.txt", "w") as file:
        file.write(text)
    with open("tfMietteet.txt", "w") as file:
        file.write(text[start:end])

    foundText = text[start:end]

    nlpOutput = nlp.annotate(text,properties={
        "annotators": "sentiment",
        "outputFormat": "json",
    })
    for s in nlpOutput["sentences"]:
        print "%d: '%s': %s %s" % (
            s["index"],
            " ".join([t["word"] for t in s["tokens"]]),
            s["sentimentValue"], s["sentiment"])



if len(sys.argv) < 2:
    print("Add path to pdf file")
else:
    print(len(sys.argv))
    print(sys.argv[1])
    pdfToText(sys.argv[1])