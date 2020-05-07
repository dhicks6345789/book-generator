#!/usr/bin/python3

# Standard libraries.
import os
import sys

# GenerateBook: Converts a collection of text and image files into a file suitible for submitting to print-on-demand services
# (e.g. Lulu.com). Depends on Pandoc.

def readFile(theFilename):
	inputHandle = open(theFilename)
	result = inputHandle.read()
	inputHandle.close()
	return result

page = 1
blankPages = 0
pageBreakString = "\n```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```\n"
rootFolder = "C:\\Users\\Administrator.KNIGHTSBRIDGESC\\Documents\\Magoo Books\\How Good Are The Martians At Fireball"
contentFolder = rootFolder + os.sep + "Content"
items = sorted(os.listdir(contentFolder))
outputHandle = open(rootFolder + os.sep + "interior.md","w")
while not items == []:
	pageItem = "Page " + str(page)
	if pageItem + ".txt" in items:
		items.remove(pageItem + ".txt")
		print(pageItem + ".txt")
		outputHandle.write(readFile(contentFolder + os.sep + pageItem + ".txt") + pageBreakString)
		blankPages = 0
		page = page + 1
	elif pageItem + ".png" in items:
		items.remove(pageItem + ".png")
		print(pageItem + ".png")
		outputHandle.write("![](" + rootFolder + os.sep + "Content" + os.sep + pageItem + ".png \"\")"+ pageBreakString)
		blankPages = 0
		page = page + 1
	else:
		print("Blank " + pageItem)
		blankPages = blankPages + 1
		page = page + 1
	if blankPages > 5:
		print("Too many blank pages. Still to process:")
		print(items)
		sys.exit(0)
outputHandle.close()
os.system("dir")
os.system("pandoc -raw_attribute -s --reference-doc=reference.docx -f markdown \"" + rootFolder + os.sep + "interior.md\" -t docx -o \"" + rootFolder + os.sep + "interior.docx\"")
