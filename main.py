from GUI import gui
from WebScraper import web_scraper
import os



path = os.path.dirname(__file__)


gui.run(web_scraper, path)