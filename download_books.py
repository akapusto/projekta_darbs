#
# Šī programma tikai lejupielade vairakas gramatas no saita www.gutenberg.org uz mapi books. Tas ir
# nepieciešams priekš dabiskas valodas analīzes(būs jāizpēta cik bieži katrs burts atkartojas reālaja tekstā)
#

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re

thisDir = Path(__file__).parent
folderDir = thisDir / 'books'
folderDir.mkdir(exist_ok = True)
downloaded_books = sum(1 for f in folderDir.iterdir() if f.is_file())
main_url = "https://www.gutenberg.org/"

i = downloaded_books
while i<=50000:
    try:
        response = requests.get(main_url + 'ebooks/' + str(i))
        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            bookName = soup.find(id = 'book_title').text + '.txt'
            bookNameForPath = re.sub(r'[\\/:*?"<>|] ', '_', bookName)
            bookPath = folderDir / bookNameForPath
            bookLinkTag = soup.find('a',string = 'Plain Text UTF-8')
            href = bookLinkTag['href']
            responseText = requests.get(main_url + href)
            if responseText.status_code == 200:
                textBytes = responseText.content
                text = textBytes.decode('utf-8')
                with open(bookPath, mode = 'w',encoding = 'utf-8') as f:
                    f.write(text)
                    print(sum(1 for f in folderDir.iterdir() if f.is_file()),'.  downloaded book: ', bookName)
                    i+=1
            else:
                print('2nd response error - ', responseText.status_code)
                i+=1
        else:
            print("1st response error - ", response.status_code)
            i+=1
    except:
        i+=1
        continue
print('ALL BOOKS WAS SUCCESFULLY DOWNLOADED')
input('press Enter to exit')
