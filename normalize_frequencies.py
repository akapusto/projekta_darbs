#
# tāpēc ka grāmatas ir ļoti daudz lieki simboli, kas ietekmē uz citu burtu
# relatīvam frekvencēm, saņemtus rezultātus ir jānotira no visiem simboliem, izņemot angļu burtus, atstarpes un dažas punktuācijas zīmes.
#
from pathlib import Path
import json as js
thisDir = Path(__file__).parent
fileDir = thisDir / 'frequencies.json'
with open(fileDir,mode='r',encoding='utf-8') as f:
    data = js.load(f).get('absolute frequencies')

dataKeys = list(data.keys()) # saņemtā vārdnīcā katra atslēga ir simbols, tāpēc dataKeys ir visu simbolu saraksts

for key in dataKeys:
    if not any(['a' <= key <= 'z',key in '.,?! ']): # ar atstarpem un punktuacijas zimem
        del data[key]
total_symbols = 0
for key in data:
    total_symbols += data[key] # skaitļojam visus simbolus no sakuma
relativeFrequency = {}
for key in data:
    relativeFrequency[key] = data[key] / total_symbols
relativeFrequency = dict(sorted(relativeFrequency.items(),key = lambda item: item[1],reverse=True))

with open(thisDir / 'SymbolFrequencies.json',mode='w',encoding='utf-8') as f:
    js.dump(relativeFrequency,f,indent=4,ensure_ascii=False)

dataKeys = list(data.keys())
for key in dataKeys:
    if not any(['a' <= key <= 'z']): # tikai ar burtiem
        del data[key]
total_symbols = 0
for key in data:
    total_symbols += data[key]
relativeFrequency = {}
for key in data:
    relativeFrequency[key] = data[key] / total_symbols
relativeFrequency = dict(sorted(relativeFrequency.items(),key = lambda item: item[1],reverse=True))
for key in relativeFrequency:
    relativeFrequency[key] = f'{round(relativeFrequency[key]*100,3)}%'

with open(thisDir / 'LetterFrequencies.json',mode='w',encoding='utf-8') as f:
    js.dump(relativeFrequency,f,indent=4,ensure_ascii=False)
