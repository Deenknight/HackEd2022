
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

    def __init__(self, adblock_path, headless = True):
        
        self.url = None

        option = Options()
        option.headless = headless
        
        super().__init__(options=option, service=FirefoxService(
            GeckoDriverManager().install()))  # make firefox browser

        self.install_addon(adblock_path)
    
    def __del__(self):
        self.quit()
        
    def download_manga(self, url, path):
        """
        Downloads the manga images into a directory as follows: path\\pagenumber.png
        
        url: url of the chapter page
        path: directory to save the path. Set to the working directory by default
        """
        
        self.get(url)

        # find the images
        chapter_img_container = self.find_element(By.XPATH, '//*[@id="chapter-images"]')
        chapter_images = chapter_img_container.find_elements(By.CLASS_NAME, "chapter-image")

        self._download_images(path, chapter_images)

    def _download_images(self, chapter_folder, images):

        index = 1
        for image in images:
            image_file = open(fr"{chapter_folder}\{index}.png", 'wb')
            image_file.write(image.screenshot_as_png)
            image_file.close()
            index += 1

    def get_cover(self, url, title, path):
        """
        Downloads the cover page to a manga_cover folder
        
        url: url of the title page
        title: title of the manga without whitespace
        path: directory to save the path. Set to the working directory by default
        """

        self.get(url)

        read_button = self.find_element(by=By.XPATH, value='//*[@id="cover"]/div[2]')

        self.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, read_button)

        body = self.find_element(by=By.XPATH, value='//*[@id="cover"]/div[1]/img')
        
        image_file = open(fr"{path}\{title}.png", 'wb')
        image_file.write(body.screenshot_as_png)
        image_file.close()

    def load_chapters(self, url):
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

        # FIXME if you print out the ultag in a debugger you'll see that not all chapters
        # are in it. We might have to load the chapters in with selenium
        for ultag in soup.find_all('ul', {'class': 'chapter-list'}):
            for litag in ultag.find_all('li'):
                titleTag = litag.find('a').get('title')
                link = litag.find('a').get('href')
                if 'https' not in link:
                    link = "mangabuddy.com/"+link  # honestly might fuck shit later
                    link =  'https://' + link.replace('//', '/') # necessary if the linktag already leads with a /
                chapter_dict[titleTag[titleTag.find('Chapter'):]] = link
        '''
        YES I KNOW THAT 2 FOR LOOPS IS REALLY STUPID BUT FOR SOME REASON 
        DOING IT THIS WAY IS FASTER, WHY?
        '''
        return chapter_dict

        

    def find_titles(self, url, user_search_input) -> dict:
        """    
        Uses the manga site's searchbar and user's input to find the manga titles on the site and returns them all as a dictionary
    
        url: url to the website's main page
        user_search_input: user's input text 
        """
        
        self.get(url)

        search_box = self.find_element(By.ID, "input-header-search")

        
        search_box.send_keys(user_search_input)

        manga_dict = self._get_manga_dict()

        return manga_dict    
    
    def _get_manga_dict(self) -> dict:
        """
        Gets all the titles that pop up in the searchbar
        
        """

        try:
            # waits for 5 seconds for the website to return search results
            WebDriverWait(self, 5).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "search-result")))
        except TimeoutException as exception:
            print("Took too long")
            print(exception)

        titles = self.find_elements(By.CLASS_NAME, "novel__item")
        manga_dict = {}

        for item in titles:
            
            title_link = item.find_element(By.PARTIAL_LINK_TEXT, '').get_attribute('href')
            title_name = item.text.split('\n')[0]

            manga_dict.update({title_name:title_link})

        return manga_dict


if __name__ == "__main__":
    import os

    main_path = os.path.dirname(__file__)
    path = os.path.join(main_path, "img")
    adblock_path = os.path.join(main_path, "utils", "ublock_origin-1.44.4.xpi")

    driver = Web_Scraping_Driver(path, adblock_path, False)

    titles = driver.find_titles("https://mangabuddy.com/", "The eminence in shadow")

    print(titles)

    