import manga_downloader as mgd
import manga_cover as mgc
import chapter_scraper as cs
import title_finder as tf


def download_manga(driver, url, title, chapter, path):
    """
    Downloads the manga images into a directory as follows: path\\title\chapter\pagenumber.png
    
    driver: webdriver to be used
    url: url of the chapter page
    title: title of the manga without whitespace
    chapter: chapter number
    path: directory to save the path. Set to the working directory by default
    """
    
    mgd.download_manga(driver, url, title, chapter, path)

def get_cover(driver, url, title, path):
    """
    Downloads the cover page to a manga_cover folder
    
    driver: webdriver to be used
    url: url of the title page
    title: title of the manga without whitespace
    path: directory to save the path. Set to the working directory by default
    """

    mgc.get_cover(driver, url, title, path)

def find_chapters(url):
    """
    Heres the run down for whoever uses this. Put link into, 
    function returns dictionary of {ChpTitle: Url}

    url: url to the website's main page
    """
    cs.find_chapters(url)

def find_titles(driver, url, user_search_input, manga_list) -> dict:
    """
    #NOTE This will need to be changed once the implementation for tkinter is finished
    
    Uses the manga site's searchbar and user's input to find the manga titles on the site and returns them all as a dictionary
    
    driver: webdriver to be used
    url: url to the website's main page
    user_search_input: user's input text 
    manga_list: graphic list element that will be updated
    """
    try:
        driver.get(url)
    except:
        print("url does not exist")

        
    tf.external_search(driver, user_search_input)

    manga_list = tf.get_manga_list(driver, manga_list)

    return manga_list    




if __name__ == "__main__":
    pass