#
# Šī programma ir realizēts primitīvs šifrēšanas algoritms, kas
# ļauj iešifrēt veselu .txt failu angļu valodā pēc noteiktas atslēgas.
# Arī ir iespējama dešifrēšana ar pareizu atslēgu
#

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path

thisDir = Path(__file__).parent

# ar lielu alfabētu bija vairākas problēmas, saistītas ar biežuma analīzi, tāpēc alfabētā
# ir tikai mazie angļu valodas simboli + atstarpes

# ALPHABET = ['o', 'Ы', '|', '"', 'И', 'd', '}', 'i', 'з', '1', ' ', '#', 'u', 'c', 'C', 'н', 'I', '%', 
#             'с', 'ё', '?', 'А', 'm', 'ч', ',', 'Р', '@', 'ш', '{', 'ф', 'Й', 'Н', 'К', 'L', 'W', 'ь', 
#             'З', 'к', 'Т', 'l', 'y', "'", 'Ъ', 'a', '<', 'Ь', 'S', 'k', '0','\\', '.', '~', '`', '&', 
#             'z', '+', 'а', 'д', 'щ', 'р', 'Ч', 'у', 'ъ', 'Э', 'г', 'T', 'Е', 'М', 'G', '_', 'Ю', 'О', 
#             'п', 'в', 'j', '8', 'Ф', 'M', 'F', 'g', 'K', 'Я', 'ю', ']', 'H', '9', 'O', 'x', 'ц', 'В', 
#             'Ш', 'J', '/', 'D', 'P', 'h', 'л', '!', 'й', 'Л', 'n', '5', 'х', 'Д', 'Б', 'и', 'v', '6', 
#             '=', 'w', 'p', 'С', 'Ё', 'E', 'X', '-', '4', 'r', 'э', 'q', '[', 'Г', 'я', 'B', 'N', 'A', 
#             '*', 'Ж', 'о', 'e', '3', ')', 'R', 'П', 'т', 'V', 'м', 'f', '>', '^', 'е', 'U', 'Щ', '2', 
#             'Y', 'b', 's', ':', 'Ц', '7', '$', 'У', 'Z', 'Q', '(', 't', ';', 'ы', 'б', 'ж', 'Х','\n']

ALPHABET = ['o', 'd', 'i', ' ', 'u', 'c',  
            'm', 
            'l', 'y', 'a', 'k', 
            'z', 'р',  
            'j', 'g', 'x', 
            'h', 'n', 'v',  
            'w', 'p', 'r', 'q', 
            'e', 'f', 
            'b', 's', 't',]

def save(text):
    #
    # saglabā tekstu jaunajā failā un atgriež Path() uz to
    #
    folder = thisDir / 'encrypted_texts'
    folder.mkdir(exist_ok=True)
    countFiles = sum(1 for file in folder.iterdir() if file.is_file())
    newFileName = folder / f'encrypter_file{countFiles}.txt'
    with open(newFileName, mode='w', encoding='utf-8') as f:
        f.write(text)
    return newFileName
def invalid_symbols(text):
    #
    # atgriež visus simbolus, kuri nav sarakstā ALPHABET
    #
    invalid_chars = ''
    for char in text:
        if char not in ALPHABET and char not in invalid_chars:
            invalid_chars += char
    return invalid_chars
def validate(text):
    #
    # notīra visu tekstu no simboliem, kuri bija atgriezti ar invalid_symbols()
    #
    invalid_chars = invalid_symbols(text)
    for char in invalid_chars:
        text = text.replace(char,'')
    return text
def crypto(text,key,mode):    # mode = 'encrypt' or 'decrypt'
    #
    # (de)šifrēšanas algoritms
    #

    text=text.lower() # parveidojam visu tekstu uz maziem burtiem, lai samazinātu unikālo simbolu skaitu šifrējamā tekstā
    text = validate(text)
    if mode == 'encrypt':
        a=1
    elif mode == 'decrypt':
        a=-1
    result = ''
    text_indexes = []
    key_indexes = []
    for char in text:
        text_indexes.append(ALPHABET.index(char))
    for char in key:
        key_indexes.append(ALPHABET.index(char))
    for i in range(len(text_indexes)):
        text_indexes[i]+=key_indexes[i%len(key_indexes)]*a
        result+=ALPHABET[text_indexes[i]%len(ALPHABET)]
    return result
def ask_file():
    global sub
    def chose(mode,source):
        global sub
        def end(text,key,mode):
            global sub
            result = crypto(text,key,mode)
            file_name = save(result)
            sub.destroy()
            sub = tk.Toplevel(root)
            sub.geometry('270x90')
            sub.title('Success!')
            ttk.Label(sub,text=f'Your text was successfully {mode}ed and saved on this path:\n{file_name}').pack()
            ttk.Button(sub,text='Thank you!',command = lambda: sub.destroy())

        sub.destroy()
        sub = tk.Toplevel(root)
        sub.geometry('270x90')
        sub.title(f'Enter {mode} key')
        ttk.Label(sub,text=f'Enter {mode} key: ').pack()
        keyEntry = ttk.Entry(sub)
        keyEntry.pack()
        btn = ttk.Button(sub,text=f'{mode}!',command = lambda: end(validate(source),keyEntry.get(),mode))
        btn.pack()
        if invalid_symbols(source):
            subsub = tk.Toplevel(sub)
            subsub.geometry('270x90')
            subsub.title('warning')
            ttk.Label(subsub,text=f'Some symbols from given text are not supported in the program.\nThose symbols were deleted from source text:').pack()
            ttk.Label(subsub,text=invalid_symbols(source)).pack()
            ttk.Button(subsub,text='Ok',command = lambda: subsub.destroy())
    global file_path
    file_path = filedialog.askopenfilename()
    with open(file_path,mode='r',encoding='utf-8') as f:
        text = f.read()
    text = text.lower()
    sub = tk.Toplevel(root)
    sub.title('Choose the mode')
    ttk.Label(sub,text = 'What are you going to do with this file?').pack()
    frame = ttk.Frame(sub)
    ttk.Button(frame,text='encrypt',command= lambda: chose('encrypt',text)).grid(column=1,row=1)
    ttk.Button(frame,text='decrypt',command=lambda: chose('decrypt',text)).grid(column=2,row=1)
    frame.pack()
root = tk.Tk()
root.title('Encrypter')
root.geometry('270x90')
file_path = ''
ttk.Label(root,text='Choose the .txt file you want be encrypted/decrypted').pack()
ttk.Button(root,text='Choose file...',command = ask_file).pack()
root.mainloop()
