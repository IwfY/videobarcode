#!/usr/bin/env python3

import argparse
import os
import sys

def extractImages(videoFilename, rate):
	'''extract images from video to directory vbc_out

	uses: ffmpeg'''
	if not 'vbc_out' in os.listdir():
		os.mkdir('vbc_out')
	command = 'ffmpeg -i \"{}\" -r {} -f image2 vbc_out/img%4d.jpg'\
				.format(videoFilename, rate)
	print('VideoBarCode: ' + command)
	ret = os.system(command)

	return ret == 0


def resizeImages():
	'''resize extracted images to be 1 pixel thin

	uses: convert (of ImageMagick)'''
	for imageFilename in os.listdir('vbc_out'):
		command = 'convert vbc_out/{} -resize 1x480\! vbc_out/{}'\
				.format(imageFilename, imageFilename)
		print('VideoBarCode: ' + command)
		ret = os.system(command)
		if ret != 0:
			return False

	return True


def composeStrip(outFilename):
	'''compose images next to each other in the right order

	uses: montage (of ImageMagick)'''
	imageList = os.listdir('vbc_out')
	for i in range(len(imageList)):
		imageList[i] = 'vbc_out/' + imageList[i]
	imageList.sort()
	imageListString = ' '.join(imageList)

	command = 'montage {} -geometry +0+0 -tile x1 \"{}.png\"'\
				.format(imageListString, outFilename)
	print('VideoBarCode: ' + command)
	ret = os.system(command)

	return True

def composeVideoStrips():
	fileList = os.listdir()
	fileList.sort()
	imageList = []
	for filename in fileList:
		if filename.endswith('.png'):
			imageList.append(filename)
	imageListString = ' '.join(imageList)

	command = 'montage {} -geometry +0+0 -tile x1 out.png'\
				.format(imageListString)
	print('VideoBarCode: ' + command)
	ret = os.system(command)

	return True


def removeTmpFiles():
	for imageFilename in os.listdir('vbc_out'):
		os.remove('vbc_out/' + imageFilename)
	os.rmdir('vbc_out')


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('files', nargs='+')
	parser.add_argument('-r', '--rate', dest='rate', default='0.2')
	args = parser.parse_args()

	for videoFile in args.files:
		if not extractImages(videoFile, args.rate):
			print('VideoBarCode: error extracting images')
			sys.exit(2)

		if not resizeImages():
			print('VideoBarCode: error resizing images')
			sys.exit(2)

		if not composeStrip(videoFile):
			print('VideoBarCode: error resizing images')
			sys.exit(2)

		removeTmpFiles()

	composeVideoStrips()


if __name__ == '__main__':
	main()
