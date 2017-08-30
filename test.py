#!/usr/bin/python
import textract
import sys

def pdfToText(pathToPdf):
    text = textract.process(pathToPdf)

    start = text.find("Toimitusjohtaja")
    end = text.find("\n\n",start)

    with open("wholeDocument.txt", "w") as file:
        file.write(text)
    with open("tfMietteet.txt", "w") as file:
        file.write(text[start:end])

if len(sys.argv) < 2:
    print("Add path to pdf file")
else:
    print(len(sys.argv))
    print(sys.argv[1])
    pdfToText(sys.argv[1])