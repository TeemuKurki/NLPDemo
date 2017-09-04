#!/usr/bin/python
import textract
import sys
from pycorenlp import StanfordCoreNLP

reload(sys)
sys.setdefaultencoding("utf-8")

def pdfToText(pathToPdf, targetText = ""):
    nlp = StanfordCoreNLP("http://localhost:9000")
    text = textract.process(pathToPdf)

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
    print(targetText)
    pdfToText(sys.argv[1],targetText)