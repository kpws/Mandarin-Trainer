#!/usr/bin/python
import random, getpass, time, os

with open(os.path.join(os.path.dirname(__file__), 'chars'),'r') as charFile:
    chars=[l.replace('\t','').rstrip('\n').rsplit(',') for l in charFile if l[0]!='#']

with open(os.path.join(os.path.dirname(__file__), 'mixChars'),'r') as mixCharFile:
    mixChars=[l.rstrip('\n') for l in mixCharFile if l[0]!='#' and not any(c[0]==l.rstrip('\n') for c in chars)]

toChinese = lambda english: chars[[c[2] for c in chars].index(english)][0]

mixCharRatio=0.1
red='\033[31m'
yellow='\033[33m'
green='\033[32m'
blue='\033[34m'
purple='\033[36m'
standard='\033[0;m'
with open(os.path.expanduser('~/.mandarinTrainerHist'),'a+') as histFile:
	hist=[l for l in histFile]
	print hist
	while True:
		if random.random()<mixCharRatio:
		    char=mixChars[random.randint(0,len(chars)-1)]
		    correct=''
		else:
		    i=random.randint(0,len(chars)-1)
		    char=chars[i][0]
		    correct=chars[i][2]
		print(yellow+char+':')
		try:
			if raw_input('')==correct:
				print(green+toChinese('right'))
				histFile.write('dd\t'+str(time.time())+'\n')
			else:
				print(red+toChinese('not')+toChinese('right')+','+
					toChinese('it')+toChinese('is')+': '+correct)
				histFile.write('ddf\n')
				if correct:
					print(blue+toChinese('pinyin')+': '+chars[i][1])
		except KeyboardInterrupt:
			print(purple+'\n'+toChinese('goodbye')+standard)
			break
