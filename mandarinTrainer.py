''' Copyright 2011 Petter Saeterskog

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

import time, os; from random import random, randrange
with open(os.path.join(os.path.dirname(__file__), 'chars'),'r') as charFile:
    chars=[l.replace('\t','').rstrip('\n').rsplit(',') for l in charFile if l[0]!='#']

toChinese=lambda english: chars[[c[2] for c in chars].index(english)][0]
termColor={'red':'31','yellow':'33','green':'32','blue':'34','turquoise':'36','std':'0;'}

def printInCol(col,text):
    print('\033['+termColor[col]+'m'+text+'\033['+termColor['std']+'m')

with open(os.path.expanduser('~/.mandarinTrainerHist'),'a+') as histFile:
    hist=[l.rstrip('\n').rsplit('\t') for l in histFile]
    lastTime=lambda charI,p:max([float(h[2]) for h in hist if h[:2]==[chars[charI][0],str(p)]]+[-1])
    active=lambda charI:lastTime(charI,0)!=-1 or lastTime(charI,1)!=-1
    probDecay=lambda charI:max(min(0.5*len(chars),5e4/(lastTime(charI,1)-lastTime(charI,0))),1.0)
    prob=lambda charI:(2.0*len(chars) if lastTime(charI,1)<lastTime(charI,0) else probDecay(charI)) if active(charI) else 1.0    
    getChar=lambda n=20,r=0,i=0:getChar(n=n-1,r=randrange(len(chars)),i=r if random()<prob(r)/prob(i) else i) if n else i
    while True:
        i=getChar()
        printInCol('yellow',chars[i][0]+':')
        try:
            if raw_input()==chars[i][2]:
                printInCol('green',toChinese('right'))
                histFile.write(chars[i][0]+'\t1'+'\t'+str(time.time())+'\n')
                hist.append([chars[i][0],'1',time.time()])
            else:
                printInCol('red',toChinese('not')+toChinese('right')+','+toChinese('it')+toChinese('is')+': '+chars[i][2])
                histFile.write(chars[i][0]+'\t0'+'\t'+str(time.time())+'\n')
                hist.append([chars[i][0],'0',time.time()])
            if chars[i][2]:
                printInCol('blue',toChinese('pinyin')+': '+chars[i][1])
        except KeyboardInterrupt:
            countType=lambda t:len([1 for i in range(len(chars)) if t(i)])
            printInCol('blue','\n'+str(countType(lambda i:True))+' '+toChinese('many'))
            printInCol('green',str(countType(lambda i:lastTime(i,1)-lastTime(i,0)>5e4))+' '+toChinese('know'))
            printInCol('yellow',str(countType(active))+' '+toChinese('use'))
            printInCol('red',str(countType(lambda i:lastTime(i,1)==-1))+' '+toChinese('not')+toChinese('use'))
            printInCol('turquoise',toChinese('goodbye'))
            break
