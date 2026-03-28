#
# Šī programma analizē lejupieladētas grāmatas un skaitļo visus simbolus, kuri pārstāv tekstā
# (tā skaitā arī punktuācijas simboli, atstarpes un pārejas uz nākamo rindu)
#
from pathlib import Path
import json
thisDir = Path(__file__).parent
folder = thisDir / 'books'
absolute_frequencies = {}
relative_frequencies = {}
counted_symbols = 0
checked_books = 0
total_books = sum(1 for f in folder.iterdir() if f.is_file()) # cik ir gramatas mapē
if folder.exists():
    print('folder "books" does exist')
    files = [f for f in folder.iterdir() if f.is_file()]
    for file in files:
        with open(file,mode='r',encoding='utf-8') as f:
            text = f.read()

            # projektā "gutenberg" visas gramatas sakas ar info par projektu, kas aiznem diezgan jūtamu daļu no visa teksta un var ietekmet
            # uz dažu burtu absoluto frekvenci, tāpēc ir jāņem tikai teksts starp fragmentiem '*** START OF  ...' un '*** END OF'
            start = text.index('*** START OF')
            start = text.index('***', start+3)+3
            end = text.index('*** END OF')
            content = text[start:end].lower()
            for char in content:
                if char in absolute_frequencies:   # ja vārdnīcā ir atslēga char
                    absolute_frequencies[char] += 1
                else:                              
                    absolute_frequencies[char] = 1 # citādi pievienojam vārdnīcai jaunu atslēgu char
                counted_symbols+=1
                relative_frequencies[char] = absolute_frequencies[char]/counted_symbols
            # json failu atjaunojam reālā laikā, lai skaitļošanas procesā jau varētu atvērt failu un
            # redzēt primārus rezultātus
            with open(thisDir / 'frequencies.json', mode='w',encoding = 'utf-8') as jsfile:
                data = {'total':counted_symbols,
                        'absolute frequencies':absolute_frequencies,   
                        'relative frequencies':relative_frequencies}
                json.dump(data,jsfile,indent=4,ensure_ascii=False)
                checked_books+=1
        print(f'checked books: {checked_books} ({round(checked_books/total_books*100,2)}%)') # attelo progresu
else:
    print('folder "books" doesn\'t exist')
input('Enter to exit')
