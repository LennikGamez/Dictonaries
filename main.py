import json
from bs4 import BeautifulSoup
import requests


data = {}
region = 'ruhrpott'

def getData():
    sesh = requests.Session()

    resp = sesh.get(f'https://www.deine-woerter.de/lexikon/{region}/')
    soup = BeautifulSoup(resp.text, 'html.parser')

    entries = soup.find_all('span', {'class':'entry'})
    for entry in entries:
        word = entry.find('abbr').text.strip()
        description = entry.find('span', {'itemprop':'description'}).text
        example = entry.find('p').text

        data.update({
            word: {
                'word': word,
                'description': description,
                'example': example
            }
        })

    sesh.close()

def parseData(dataSet):
    newDict = {}
    for i in dataSet:
        # # ignore words with more than 1 space
        # if i.count(' ') > 1:
        #     continue

        newDict.update({i:dataSet.get(i)})
    return newDict

def writeData(file, data):
    with open(file, "w+", encoding='utf-8') as f:
       f.write(json.dumps(data, ensure_ascii=False, indent=4)) 

def main():
    getData()
    newData = parseData(data)
    writeData(f'{region.capitalize()}.json', newData)

if __name__ == '__main__':
    main()