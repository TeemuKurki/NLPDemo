#!/usr/bin/python
import textract
import sys
import urllib2
from pycorenlp import StanfordCoreNLP

reload(sys)
sys.setdefaultencoding("utf-8")

def download_pdf(pdfUrl, targetText = ""):
    response = urllib2.urlopen(pdfUrl)
    file = open("../document.pdf", "w")
    file.write(response.read())
    file.close
    pdfToText(targetText)
    print("Completed")

def pdfToText(targetText):
    nlp = StanfordCoreNLP("http://localhost:9000")
    text = textract.process("../document.pdf")

    print(targetText)

    start = text.find(targetText)
    end = text.find("\n\n",start)

    with open("wholeDocument.txt", "w") as file:
        file.write(text)
    with open("tfMietteet.txt", "w") as file:
        file.write(text[start:end])

    if targetText != "":
        foundText = text[start:end]
    else:
        foundText = text
    nlpOutput = nlp.annotate(foundText,properties={
        "annotators": "sentiment",
        "outputFormat": "json",
    })

    for s in nlpOutput["sentences"]:
        print "%d: '%s': %s %s" % (
            s["index"],
            " ".join([t["word"] for t in s["tokens"]]),
            s["sentimentValue"], s["sentiment"])


if len(sys.argv) < 2:
    print("Add atleast Pdf file and possible search argument(s)")
else:
    print(sys.argv[1])
    targetText = " ".join(sys.argv[2::])
    download_pdf(sys.argv[1],targetText)