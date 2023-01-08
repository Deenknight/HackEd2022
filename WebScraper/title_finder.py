#selenium
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



def external_search(driver, user_search_input):
    """
    Inputs the user input into the webdriver's searchbar
    
    driver: webdriver to be used
    user_search_input: user's input text  
    """

    mangas = driver.find_element(By.ID, "input-header-search")

    #NOTE check if this still works with tkinter or has to be changed
    mangas.send_keys(user_search_input)


def get_manga_list(driver, manga_list) -> dict:
    """
    Gets all the titles that pop up in the searchbar
    
    driver: webdriver to be used
    manga_list: graphic list element that will be updated
    """

    try:
        #waits for 5 seconds for the website to return search results
        WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "search-result")))
    except TimeoutException as exception:
        print(exception)

    names = driver.find_elements(By.CLASS_NAME, "novel__item")
    manga_dict = {}

    for item in names:
        #if the current item in 'names' had a header tag_name, then the item is both added to 
        #'manga_list' (the title is added) and added to 'manga_dict'  (title and url)
        if item.find_element(By.XPATH, "./..").tag_name != "p":
            dict_value = item.find_element(By.PARTIAL_LINK_TEXT, '').get_attribute('href')
            
            #FIXME change depending on how tkinter uses list widgets
            manga_list.addItem(item.text)

            manga_dict.update({item.text:dict_value})

    return manga_dict
    