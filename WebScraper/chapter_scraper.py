from bs4 import BeautifulSoup
import requests
import re


def find_chapters(url):
    '''
    Heres the run down for whoever uses this. Put link into, 
    function returns dictionary of {ChpTitle: Url}

    url: url to the website's main page
    '''
    chapterDict = {}
    # load the page into html_text
    html_text = requests.get(url)

    # parse the text using the lxml parser
    soup = BeautifulSoup(html_text.text, 'lxml')

    for ultag in soup.find_all('ul', {'class': 'chapter-list'}):
        for litag in ultag.find_all('li'):
            titleTag = litag.find('a').get('title')
            link = litag.find('a').get('href')
            if 'https' not in link:
                link = "https://mangabuddy.com"+link  # honestly might fuck shit later
            chapterDict[titleTag[titleTag.find('Chapter'):]] = link
    '''
    YES I KNOW THAT 2 FOR LOOPS IS REALLY STUPID BUT FOR SOME REASON 
    DOING IT THIS WAY IS FASTER, WHY?
    '''
    return chapterDict


if __name__ == "__main__":
    chapterDict = find_chapters(
        "https://mangabuddy.com/mbx13-chainsaw-man")
    print(chapterDict)
