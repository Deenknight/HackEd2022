
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import requests


class Web_Scraping_Driver(webdriver.Firefox):

    def __init__(self, path, adblock_path, headless = True):
        
        
        self.path = path
        self.url = None

        option = Options()
        option.headless = headless
        
        super().__init__(options=option, service=FirefoxService(
            GeckoDriverManager().install()))  # make firefox browser

        self.install_addon(adblock_path)
    
    def __del__(self):
        self.quit()
        
    def download_manga(self, url, title, chapter):
        """
        Downloads the manga images into a directory as follows: path\\title\chapter\pagenumber.png
        
        driver: webdriver to be used
        url: url of the chapter page
        title: title of the manga without whitespace
        chapter: chapter number
        path: directory to save the path. Set to the working directory by default
        """
        
        self.get(url)

        # find the images
        chapter_img_container = self.find_element(By.XPATH, '//*[@id="chapter-images"]')
        chapter_images = chapter_img_container.find_elements(By.CLASS_NAME, "chapter-image")

        self.download_images(f"{self.path}\\{title}\\{chapter}", chapter_images)

    def download_images(self, chapter_folder, images):

        index = 0
        for image in images:
            image_file = open(fr"{chapter_folder}\{index}.png", 'wb')
            image_file.write(image.screenshot_as_png)
            image_file.close()
            index += 1

    def get_cover(self, url, title):
        """
        Downloads the cover page to a manga_cover folder
        
        driver: webdriver to be used
        url: url of the title page
        title: title of the manga without whitespace
        path: directory to save the path. Set to the working directory by default
        """

        self.get(url)

        body = self.find_element(by=By.XPATH, value='//*[@id="cover"]/div[1]/img')
        body.screenshot(f"{self.path}\\{title}.png")

    def load_chapters(url):
        """
        Heres the run down for whoever uses this. Put link into, 
        function returns dictionary of {ChpTitle: Url}

        url: url to the website's main page
        """
        chapter_dict = {}
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
                chapter_dict[titleTag[titleTag.find('Chapter'):]] = link
        '''
        YES I KNOW THAT 2 FOR LOOPS IS REALLY STUPID BUT FOR SOME REASON 
        DOING IT THIS WAY IS FASTER, WHY?
        '''
        return chapter_dict

        

    def find_titles(self, url, user_search_input, manga_list) -> dict:
        """
        #NOTE This will need to be changed once the implementation for tkinter is finished
        
        Uses the manga site's searchbar and user's input to find the manga titles on the site and returns them all as a dictionary
        
        driver: webdriver to be used
        url: url to the website's main page
        user_search_input: user's input text 
        manga_list: graphic list element that will be updated
        """
        
        self.get(url)

        mangas = self.find_element(By.ID, "input-header-search")

        #NOTE check if this still works with tkinter or has to be changed
        mangas.send_keys(user_search_input)

        manga_list = self.get_manga_list(self, manga_list)

        return manga_list    
    
    def get_manga_list(driver, manga_list) -> dict:
        """
        Gets all the titles that pop up in the searchbar
        
        driver: webdriver to be used
        manga_list: graphic list element that will be updated
        """

        try:
            # waits for 5 seconds for the website to return search results
            WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "search-result")))
        except TimeoutException as exception:
            print(exception)

        names = driver.find_elements(By.CLASS_NAME, "novel__item")
        manga_dict = {}

        for item in names:
            # if the current item in 'names' had a header tag_name, then the item is both added to 
            # 'manga_list' (the title is added) and added to 'manga_dict'  (title and url)
            if item.find_element(By.XPATH, "./..").tag_name != "p":
                dict_value = item.find_element(By.PARTIAL_LINK_TEXT, '').get_attribute('href')
                
                #FIXME change depending on how tkinter uses list widgets
                manga_list.addItem(item.text)

                manga_dict.update({item.text:dict_value})

        return manga_dict
