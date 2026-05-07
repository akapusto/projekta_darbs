import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path
from math import gcd
import json

thisDir = Path(__file__).parent
decryptedBooksDir = thisDir / 'decrypted_books'
decryptedBooksDir.mkdir(exist_ok = True)
filesInFolder = sum(1 for f in decryptedBooksDir.iterdir() if f.is_file())
ALPHABET = ['a','b','c','d','e','f','g',
            'h','i','j','k','l','m','n',
            'o','p','q','r','s','t','u',
            'v','w','x','y','z']
def evaluateResult(text, frequencyTable):
    textFrequencies = {}
    total = len(text)
    for c in text:
        textFrequencies[c] = textFrequencies.get(c,0) + 1
    score = 0
    for c in textFrequencies:
        frequencyIs = textFrequencies[c] / total
        frequencyShouldBe = float(frequencyTable.get(c, 0))/100
        score -= abs(frequencyIs - frequencyShouldBe)
    return score

def gcd_of_distances(lst):
    g = 0
    for i in range(len(lst)-1):
        dist = lst[i+1] - lst[i]
        g = gcd(g, dist)
    return g
def ngramsFromText(text, n):
    #
    # noķer visus burtu savienojumus no n burtiem
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
    # filtrē n-grammas, kas atkartojas vismaz divas reizes
    #
    repeating_ngrams = {}
    for ngram in ngrams:
        if len(ngrams[ngram])>1:
            repeating_ngrams[ngram] = ngrams[ngram]
    repeating_ngrams = dict(sorted(repeating_ngrams.items(),key = lambda item: len(item[1])))
    return repeating_ngrams
def differences(lst):
    #
    # skaitļo visas iespējamas starpības starp diviem elementiem sarakstā
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
    lght = len(ngrams)                            #
    i=0                                           #
    for ngram in ngrams:
        i+=1
        print(i/lght*100, '%')                    #
        root.update()                             #
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
def decryptCaesar(text, key):
    # key in range(26)
    result = []
    for char in text:
        if char in ALPHABET:
            charIndex = ALPHABET.index(char)
            result.append(ALPHABET[(charIndex-key) % len(ALPHABET)])
    return ''.join(result)
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
    klen = keys[1]
    ttk.Label(sub,text=f'Key\'s lenght is {klen}.').pack()
    ttk.Button(sub,text=f'Ok',command = lambda: sub.destroy())
    startdecryptbtn.pack()
def decryptVigenere():
    if not (thisDir/'frequencies.json').exists():
        print('frequency table wasn\'t found')
        return
    with open(thisDir/'frequencies.json', mode='r', encoding='utf-8') as f:
        frequencyTable = json.load(f)
    with open(chosenFile, mode='r', encoding='utf-8') as f:
        text = f.read()
    fragments = ['' for i in range(klen)]
    for i in range(len(text)):
        fragments[i % klen] += text[i]
    decrypted_fragments = []
    for fragment in fragments:
        best_score = -100
        best_text = ""
        for shift in range(26):
            candidate = decryptCaesar(fragment, shift)
            score = evaluateResult(candidate, frequencyTable)
            if score > best_score:
                best_score = score
                best_text = candidate
        decrypted_fragments.append(best_text)
    decrypted_text = ""
    for i in range(len(text)):
        decrypted_text += decrypted_fragments[i % klen][i // klen]
    with open(decryptedBooksDir / f'decrypted_book{filesInFolder+1}.txt',
              mode='w', encoding='utf-8') as f:
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
