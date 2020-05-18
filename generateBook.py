#!/usr/bin/python3

# Standard libraries.
import os
import sys

# GenerateBook: Converts a collection of text, image and audio files into a variety of formats, including print-ready PDFs suitible for
# submitting to print-on-demand services (e.g. Lulu.com). Depends on Pandoc, WeasyPrint, ffmpeg.

def readFile(theFilename):
	inputHandle = open(theFilename)
	result = inputHandle.read()
	inputHandle.close()
	return result

pageBreakString = "\n```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```\n"

if len(sys.argv) < 2:
	print("Usage: generateBook [rootFolder]")
	print("This script expects to find a sub-folder called \"content\" containing files named Page 1, Page 2, etc.")
	sys.exit(0)

rootFolder = sys.argv[1]
contentFolder = rootFolder + os.sep + "Content"

page = 1
blankPages = 0
textFiles = []
imageFiles = []
audioFiles = []
audioTransition = None
items = sorted(os.listdir(contentFolder))
if "transition.wav" in items:
	items.remove("transition.wav")
	audioTransition = "transition.wav"

# Sort through the items in the input folder, creating (ordered) lists as we go of media to include in different versions of this book.
while not items == []:
	pageItem = "Page " + str(page)
	pageFound = False
	if pageItem + ".txt" in items:
		items.remove(pageItem + ".txt")
		textFiles.append(pageItem + ".txt")
		pageFound = True
	if pageItem + ".png" in items:
		items.remove(pageItem + ".png")
		imageFiles.append(pageItem + ".png")
		pageFound = True
	if pageItem + ".wav" in items:
		items.remove(pageItem + ".wav")
		audioFiles.append(pageItem + ".wav")
		pageFound = True
		
	if pageFound:
		blankPages = 0
		page = page + 1
	else:
		blankPages = blankPages + 1
		page = page + 1
		
	if blankPages > 5:
		print("Too many blank pages. Still to process:")
		print(items)
		sys.exit(0)

# Generate video-with-audio version.
for audioFile in audioFiles:
	print(audioFile[:-3])

#outputHandle = open(rootFolder + os.sep + "interior.md","w")
#outputHandle.close()
#os.system("pandoc -raw_attribute -s --reference-doc=reference.docx -f markdown \"" + rootFolder + os.sep + "interior.md\" -t docx -o \"" + rootFolder + os.sep + "interior.docx\"")

#outputHandle.write(readFile(contentFolder + os.sep + pageItem + ".txt") + pageBreakString)
#outputHandle.write("![](" + rootFolder + os.sep + "Content" + os.sep + pageItem + ".png \"\")"+ pageBreakString)
