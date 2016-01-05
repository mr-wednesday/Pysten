#!/usr/bin/python
import sys
from PIL import Image
import hashlib

#Needs numpy and standart Python libraries

def convertSHA(key):
	#Hash the key via SHA256
	return hashlib.sha256(key).hexdigest()

def unglueN(line,n):
	return [line[i:i+n] for i in range(0, len(line), n)]

def hideMessage(message):
	#Convert plain text to ascii array
	ascii = []
	for char in message:
		ascii.append(ord(char))
		#print ord(char)
	return ascii

def fixKey(key,message):
	#If the key length is lesser than the message, duplicate it until it reaches the same length
	while len(key)<len(message):
		#print len(key), len(message)
		difference = len(message)-len(key)
		keyarr=list(key)
		firstN = keyarr[:difference]
		key=key+''.join(firstN)
	return key

def encode(im,pixels,message,key):
	arr=[]
	i=0
	j=0
	for pixel in pixels:
		if i<len(message):
			#Process the first len(message) pixels only
			sump= message[i]+key[i]
			#Encrypt
			arr.append((pixel[0], pixel[1], pixel[2], sump))
			#Alter the Alpha channel value
			j+=1
			#Post increment
		i+=1
		#Post Increment
	im.putdata(arr)
	#Glue the array
	im.save('Pysten_'+sys.argv[2].split('.')[0]+'.png')
	#Save the output

def decode(im,pixels,key):
	arr=[]
	i=0
	j=0
	for pixel in pixels:
		if i<len(key):
			#Process the first len(key) pixels only
			message=pixel[3]-key[i];
			#Decrypt
			arr.append(chr(message))
			#Append the character to array
			j+=1
			#Post Increment
		i+=1
		#Post Increment
	print '\nMessage:'
	print ''.join(arr)+'\n'
	print printDetails(im)

def main():
	message= ' '.join(sys.argv[4:len(sys.argv)])
	key = sys.argv[3]
	key = convertSHA(key)
	option = sys.argv[1]
	#allow whitespaces for the message
	#argv[1]=option, argv[2]=image file, argv[3]=key, argv[4]=argv[max]=message
	if(option)=='encode':
		key=fixKey(key,message)
	#Hash key
	im = Image.open(sys.argv[2]).convert('RGBA')
	#Add the alpha channel
	width, height = im.size
	mode = im.mode

	message = hideMessage(message)
	key = hideMessage(key)
	pixels = list(im.getdata())
	#2D Pixel array
	if(option)=='encode':
		encode(im,pixels,message,key)

	if(option)=='decode':
		decode(im,pixels,key)
	#Parse options
def printDetails(im):
	#Print details
	print '########################'
	print 'Image size:',im.size
	print 'Image mode:',im.mode
	
'''
For Future work
def toByteStr(message):
	return ' '.join(format(x, 'b') for x in bytearray(message));

def toByteArr(message):
	return map(ord,bytearray(message));
def sumSeries(key):
	i=0
	print(key)
	for number in key:
		if(i!=0):
			number+=key[i-1]
			key[i]=number
		i+=1
	print(key)
'''
if __name__ == '__main__':
	main()