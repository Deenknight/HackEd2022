from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import os

def get_cover(driver, url, title, path = os.path.dirname(__file__)):
    """
    Downloads the cover page to a manga_cover folder
    
    driver: webdriver to be used
    url: url of the title page
    title: title of the manga without whitespace
    path: directory to save the path. Set to the working directory by default
    """
    
    
    driver.get(url)

    take_screenshots(driver, path+"\manga_covers", title)
    

def take_screenshots(driver: webdriver.Firefox, path: str, title):
    if not os.path.exists(path):
        os.makedirs(path)

    body = driver.find_element(by=By.XPATH, value='//*[@id="cover"]/div[1]/img')
    body.screenshot(f"{path}\\{title}.png")
    

if __name__ == "__main__":
    path = os.path.dirname(__file__)
    option = Options()
    option.headless = False
    driver = webdriver.Firefox(options=option, service=Service(path + "\geckodriver.exe")) # make firefox browser
    adblockPath = path+"\\ublock_origin-1.44.4.xpi" 

    driver.install_addon(adblockPath)

    website = "https://mangabuddy.com/youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-e"
    title = "youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-e"
    get_cover(driver, website, title)

    driver.close()