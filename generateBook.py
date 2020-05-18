#!/usr/bin/python3

# Standard libraries.
import os
import sys
import math
import shutil

# PIL - the Python Image Library, used for bitmap image manipulation.
import PIL
import PIL.Image

# PyDub - Python audio file manipulation library.
import pydub



# GenerateBook: Converts a collection of text, image and audio files into a variety of formats, including print-ready PDFs suitible for
# submitting to print-on-demand services (e.g. Lulu.com). Depends on Pandoc, WeasyPrint, ffmpeg, PIL, pydub.

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

# Generate video-with-audio version. Define the resolution, in pixels, of image to map to each page.
pageImageWidth = 512
pageImageHeight = 512
if not audioFiles == []:
	os.makedirs("temp", exist_ok=True)
	transitionAudio = None
	transitionDuration = 0
	if not audioTransition == None:
		transitionAudio = pydub.AudioSegment.from_wav(contentFolder + os.sep + "transition.wav")
		transitionDuration = math.ceil(transitionAudio.duration_seconds)
		padLength = int(round((float(transitionDuration) - transitionAudio.duration_seconds) * float(1000)))
		transitionAudio = transitionAudio + pydub.AudioSegment.silent(duration=padLength)
	itemCount = 0
	outputWav = None
	ffmpegCommand = "ffmpeg -y"
	for audioFile in audioFiles:
		if audioFile[:-4] + ".png" in imageFiles:
			itemCount = itemCount + 1
			
			pageImage = PIL.Image.new("RGB", (pageImageWidth, pageImageHeight), "white")
			inputImage = PIL.Image.open(contentFolder + os.sep + audioFile[:-4] + ".png")
			pageImage.paste(inputImage.resize((pageImageWidth,pageImageHeight)), box=(0,0,pageImageWidth,pageImageHeight))
			pageImage.save("temp" + os.sep + str(itemCount) + ".png")
			inputImage.close()
			pageImage.close()

			pageAudio = pydub.AudioSegment.from_wav(contentFolder + os.sep + audioFile[:-4])
			if outputWav == None:
				outputWav = pageAudio
			else:
				outputWav = outputWav + pageAudio

			paddedDuration = math.ceil(outputWav.duration_seconds)
			padLength = int(round((float(paddedDuration) - outputWav.duration_seconds) * float(1000)))
			print(audioFile[:-4] + ": " + str(pageAudio.duration_seconds) + " long, padded to " + str(paddedDuration) + " with " + str(padLength) + " milliseconds.")
			outputWav = outputWav + pydub.AudioSegment.silent(duration=padLength)
			if not transitionAudio == None:
				outputWav = outputWav + transitionAudio
			print(outputWav.duration_seconds)

			ffmpegCommand = ffmpegCommand + " -loop 1 -t " + str(math.ceil(pageAudio.duration_seconds) + transitionDuration) + " -i \"temp\\" + str(itemCount) + ".png\""

	# See: https://superuser.com/questions/1283713/create-video-from-images-and-audio-with-varying-image-durations-using-ffmpeg
	outputWav.export("temp" + os.sep + "audio.wav", format="wav")
	ffmpegCommand = ffmpegCommand + " -i temp" + os.sep + "audio.wav -filter_complex \"concat=n=" + str(itemCount) + "\" -shortest -c:v libx264 -pix_fmt yuv420p -c:a aac \"" + rootFolder + os.sep + "slideshow.mp4\""
	print(ffmpegCommand)
	#os.system(ffmpegCommand)

	shutil.rmtree("temp")

#outputHandle = open(rootFolder + os.sep + "interior.md","w")
#outputHandle.close()
#os.system("pandoc -raw_attribute -s --reference-doc=reference.docx -f markdown \"" + rootFolder + os.sep + "interior.md\" -t docx -o \"" + rootFolder + os.sep + "interior.docx\"")

#outputHandle.write(readFile(contentFolder + os.sep + pageItem + ".txt") + pageBreakString)
#outputHandle.write("![](" + rootFolder + os.sep + "Content" + os.sep + pageItem + ".png \"\")"+ pageBreakString)
