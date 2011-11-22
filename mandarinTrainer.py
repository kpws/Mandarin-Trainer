#!/usr/bin/python
import random, getpass, time, os

with open(os.path.join(os.path.dirname(__file__), 'chars'),'r') as charFile:
    chars=[l.replace('\t','').rstrip('\n').rsplit(',') for l in charFile if l[0]!='#']

with open(os.path.join(os.path.dirname(__file__), 'mixChars'),'r') as mixCharFile:
    mixChars=[l.rstrip('\n') for l in mixCharFile if l[0]!='#' and not any(c[0]==l.rstrip('\n') for c in chars)]

toChinese = lambda english: chars[[c[2] for c in chars].index(english)][0]

mixCharRatio=0.1

with open(os.path.expanduser('~/.mandarinTrainerHist'),'ra+') as histFile:
	hist=[l for l in histFile]
	print hist
	done=0
	correct=0
	while True:
		try:
			if random.random()<mixCharRatio:
				print('\033[33m'+mixChars[random.randint(0,len(chars)-1)]+':'+'\033[0;m')
				if raw_input('')=='':
					print('\033[32m'+toChinese('right')+'\033[0;m')
					correct+=1
					histFile.write('dd\t'+str(time.time())+'\n')
				else:
					print('\033[31m'+toChinese('not')+toChinese('right')+','+
						toChinese('it')+toChinese('is')+':\033[0;m')
					histFile.write('ddf\n')
			else:
				i=random.randint(0,len(chars)-1)
				print('\033[33m'+chars[i][0]+':'+'\033[0;m')
				if raw_input('').lower()==chars[i][2]:
					print('\033[32m'+toChinese('right')+'\033[0;m')
					correct+=1
					histFile.write('asdf\n')
				else:
					print('\033[31m'+toChinese('not')+toChinese('right')+','+
						toChinese('it')+toChinese('is')+': '+chars[i][2]+'\033[0;m')
					histFile.write('fefe\n')
				print('\033[34m'+toChinese('pinyin')+': '+chars[i][1]+'\033[0;m')
			done+=1
		except KeyboardInterrupt:
			if done:
				print('\n'+str(correct*100//done)+'% '+toChinese('right'))
				if correct*100>=done*95:
					print(toChinese('very')+toChinese('good'))
			print(toChinese('goodbye'))
			break
