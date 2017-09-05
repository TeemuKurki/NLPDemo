#!/usr/bin/python
import textract
import sys
import urllib2
import os
from pycorenlp import StanfordCoreNLP

import json

reload(sys)
sys.setdefaultencoding("utf-8")

def download_pdf(pdfUrl, targetText = ""):
    response = urllib2.urlopen(pdfUrl)
    with open("document.pdf","w") as file:
        file.write(response.read())
    pdfToText(targetText)
    os.remove("document.pdf")
    print("Completed")

def pdfToText(targetText):
    nlp = StanfordCoreNLP("http://localhost:9000")
    text = textract.process("document.pdf")

    #with open("txtFromPdf.txt","w") as file:
    #    file.write(text)


    if targetText != "":
        start = text.find(targetText)
        end = text.find("\n\n",start)

        foundText = text[start:end]
    else:
        foundText = text

    nlpOutput = nlp.annotate(foundText,properties={
        "annotators": "sentiment, ssplit",
        "outputFormat": "json",
    })

    #with open("nlpOutput.json", "w") as file:
    #    json.dump(nlpOutput, file)

    sentimentCounter = 0.0
    for s in nlpOutput["sentences"]:

        sentence = " ".join([t["word"] for t in s["tokens"]])
        sentenceSentimentValue = s["sentimentValue"]
        sentenceSentiment =s["sentiment"]

        print sentence, sentenceSentimentValue, sentenceSentiment

        sentimentCounter += float(sentenceSentimentValue)

    print "\n0 Very Negative, 1 Negative, 2 Neutral, 3 Positive, 4 Very Positive"
    print "{}: {}".format("Sentiment: ", sentimentCounter/len(nlpOutput["sentences"]))

if len(sys.argv) < 2:
    print("Add atleast Pdf file and possible search argument(s)")
else:
    targetText = " ".join(sys.argv[2::])
    download_pdf(sys.argv[1],targetText)