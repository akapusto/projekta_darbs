#
# Ši programmā dešifrēs iešifrēto failu pie nezināmas atslēgas
#


import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path
from math import gcd
import json

thisDir = Path(__file__).parent

def ngramsFromText(text, n):
    #
    # catches all sequences of n letters
    #
    ngrams = {}
    for i in range(len(text)+1-n):
        if text[i:i+n] not in ngrams:
            ngrams[text[i:i+n]] = [i]
        else:
            ngrams[text[i:i+n]].append(i)
    return ngrams
def repeatingngrams(ngrams):
    #
    # catches all letter sequences whith repeats more than once
    #
    repeating_ngrams = {}
    for ngram in ngrams:
        if len(ngrams[ngram])>1:
            repeating_ngrams[ngram] = ngrams[ngram]
    repeating_ngrams = dict(sorted(repeating_ngrams.items(),key = lambda item: len(item[1]))) # sortes dictionary by element's value's lenght
    return repeating_ngrams
def differences(lst):
    #
    # counts all possible differences between 2 elements in given list
    #
    differences = []
    for el1 in lst:
        for el2 in lst:
            if el1 != el2:
                differences.append(abs(el1-el2))
    return differences
def keyLenghtCandidates(text):
    #
    # calculates candidates for encrypting key lenght
    #
    ngrams = repeatingngrams(ngramsFromText(text,n=3))
    candidate_list = {}
    for ngram in ngrams:
        intervals = differences(ngrams[ngram])
        if len(intervals)>1:
            candidate = gcd(*intervals)
        else:
            continue
        if candidate not in candidate_list:
            candidate_list[candidate] = 1
        else:
            candidate_list[candidate] +=1
    candidate_list = dict(sorted(candidate_list.items(),key= lambda item: item[1],reverse=True))
    return candidate_list
def decryptCaesar(text,frequencyTable = None):
    if not (thisDir/'SymbolFrequencies.json').exists() and frequencyTable == None:
        print('frequency table wasn\'t found')
        return
    if frequencyTable == None:
        with open(thisDir/'SymbolFrequencies.json',mode='r',encoding='utf-8') as f:
            frequencyTable = json.load(f)
    textFrequencies = {}
    for char in text:
        if char not in textFrequencies:
            textFrequencies[char] = 1
        else:
            textFrequencies[char] +=1
    relativeTextFrequencies = {char: textFrequencies[char]/len(text) for char in textFrequencies}
    relativeTextFrequencies = dict(sorted(relativeTextFrequencies.items(),key = lambda item: item[1],reverse=True))
    charsText = list(relativeTextFrequencies.keys())
    charsStatistics = list(frequencyTable.keys())
    translateTable = {charsText[i]: charsStatistics[i] for i in range(min(len(charsText),len(charsStatistics)))}
    decryptedText = text.translate(str.maketrans(translateTable))
    return decryptedText
def chooseFile():
    global chosenFile
    chosenFile = filedialog.askopenfilename()
    if chosenFile:
        frame1 = ttk.Frame(root)
        lbl1 = ttk.Label(frame1,text='Chosen file: ')
        lbl2 = ttk.Label(frame1,text=chosenFile)
        lbl1.grid(column=1,row=1)
        lbl2.grid(column=2,row=1)
        frame1.pack()
        btn.pack()
def kasiskiMethod():
    global klen
    process_lbl = ttk.Label(root,text='Analyzing... It may take some time.')
    process_lbl.pack()
    root.update()
    if not chosenFile:
        return
    with open(chosenFile,mode='r',encoding='utf-8') as f:
        text= f.read()
    candidates = keyLenghtCandidates(text)
    sub = tk.Toplevel(root)
    sub.title('Key\'s lenght\'s candidates')
    sub.geometry('400x300')
    if len(candidates) > 5:
        showCandidates = 5
    else:
        showCandidates = len(candidates)
    keys = list(candidates.keys())
    frame2 = ttk.Frame(sub)
    for i in range(showCandidates+1):
        ttk.Label(frame2,text=f'{i+1}. key\'s length\'s candidate: {keys[i]}').grid(column=1,row=i+1)
        ttk.Label(frame2,text=f'({candidates[keys[i]]})').grid(column=2,row=i+1)
    frame2.pack()
    process_lbl.destroy()
    klen = keys[0]
    ttk.Label(sub,text=f'The most popular key\'s lenght was {keys[0]}.\nIt will be used further for decrypting algorhytm.').pack()
    ttk.Button(sub,text=f'Ok',command = lambda: sub.destroy())
    startdecryptbtn.pack()
def decryptVigenere():
    #
    # balstoties uz citās programmās izskaitļotas frekvenču tabulas mēģina dešifrēt tekstu
    #
    if not (thisDir/'SymbolFrequencies.json').exists():
        print('frequency table wasn\'t found')
        return
    with open(thisDir/'frequencies.json',mode='r',encoding='utf-8') as f:
        frequencyTable = json.load(f)['relative frequencies']
        frequencyTable = dict(sorted(frequencyTable.items(),key=lambda item: item[1],reverse=True))
    with open(chosenFile,mode='r',encoding='utf-8') as f:
        text= f.read()
    splitted_text = ['' for i in range(klen)]
    for i in range(len(text)):
        splitted_text[i%klen]+=text[i]
    decrypted_splitted_text = []
    for fragment in splitted_text:
        decrypted_splitted_text.append(decryptCaesar(fragment,frequencyTable))
    decrypted_text=''
    for i in range(len(text)):
        decrypted_text += decrypted_splitted_text[i%klen][i//klen]
    with open('DECRYPTEDD.txt',mode='w',encoding='utf-8') as f:
        f.write(decrypted_text)
    
root = tk.Tk()
root.title('Decrypt')
root.geometry('400x300')
chosenFile = ''
klen = 0 # found key's length
btn = ttk.Button(root,text='Find key\'s lenght',command=kasiskiMethod)
startdecryptbtn = ttk.Button(root,text=f'Start decrypting!', command = decryptVigenere)
ttk.Button(root,text='Choose encrypted file',command = chooseFile).pack()

root.mainloop()
