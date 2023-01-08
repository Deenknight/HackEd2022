
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException

import os
import time
import sys

def download_manga(driver, url, title, chapter, path = os.path.dirname(__file__)+"\\manga"):
    """
    Downloads the manga as a set of images

    driver: webdriver to be used
    url: url of the chapter page
    title: title of the manga without whitespace
    chapter: chapter number
    path: path to the download location
    """
    

    # load the site
    driver.get(url)


    # find the images
    chapter_img_container = driver.find_element(By.XPATH, '//*[@id="chapter-images"]')
    chapter_images = chapter_img_container.find_elements(By.CLASS_NAME, "chapter-image")

    download_images(f"{path}\\{title}\\{chapter}", chapter_images)


def download_images(chapter_folder, images):
    if not os.path.exists(chapter_folder):
        os.makedirs(chapter_folder)

    index = 0
    for image in images:
        image_file = open(f"{chapter_folder}\\{index}.png", 'wb')
        image_file.write(image.screenshot_as_png)
        image_file.close()
        index += 1
    
    


if __name__ == "__main__":
    path = os.path.dirname(__file__)
    option = Options()
    option.headless = False
    driver = webdriver.Firefox(options=option, service=FirefoxService(
        GeckoDriverManager().install()))  # make firefox browser

    adblockPath = path+"\\ublock_origin-1.44.4.xpi"
    driver.install_addon(adblockPath)
    



    url = "https://mangabuddy.com/the-eminence-in-shadow/chapter-46"
    title = "the-eminence-in-shadow"
    chapter = 46
    path = os.path.dirname(__file__)

    download_manga(driver, url, title, chapter)

    driver.close()
