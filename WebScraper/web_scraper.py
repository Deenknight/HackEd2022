from .manga_downloader import download_manga
from .manga_cover import download_cover
from .chapter_scraper import find_chapters
from .title_finder import external_search, get_manga_list

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import os

def download_manga(driver, url, title, chapter, path):
    """
    Downloads the manga images into a directory as follows: path\\title\chapter\pagenumber.png
    
    driver: webdriver to be used
    url: url of the chapter page
    title: title of the manga without whitespace
    chapter: chapter number
    path: directory to save the path. Set to the working directory by default
    """
    
    download_manga(driver, url, title, chapter, path)

def get_cover(driver, url, title, path):
    """
    Downloads the cover page to a manga_cover folder
    
    driver: webdriver to be used
    url: url of the title page
    title: title of the manga without whitespace
    path: directory to save the path. Set to the working directory by default
    """

    download_cover(driver, url, title, path)

def load_chapters(url):
    """
    Heres the run down for whoever uses this. Put link into, 
    function returns dictionary of {ChpTitle: Url}

    url: url to the website's main page
    """
    chapters_dict = find_chapters(url)

    return chapters_dict

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

        
    external_search(driver, user_search_input)

    manga_list = get_manga_list(driver, manga_list)

    return manga_list    

def create_driver():
    path = os.path.dirname(__file__)
    option = Options()
    option.headless = False
    driver = webdriver.Firefox(options=option, service=FirefoxService(
        GeckoDriverManager().install()))  # make firefox browser

    adblockPath = path+"\\ublock_origin-1.44.4.xpi"
    driver.install_addon(adblockPath)

    return driver

def delete_driver(driver):
    driver.close()
    del driver

if __name__ == "__main__":
    pass