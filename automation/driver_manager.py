from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pathlib import Path

class DriverManager:
    
    def __init__(self, download_dir="./downloads"):
        self.download_dir = Path(download_dir).absolute()
        self.download_dir.mkdir(exist_ok=True)
        self.driver = None

    def setup_driver(self):
        firefox_options = Options()
        firefox_options.set_preference("browser.download.folderList", 2)
        firefox_options.set_preference("browser.download.dir", str(self.download_dir))
        firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", 
                                     "application/pdf,application/octet-stream,application/x-pdf,application/vnd.pdf")
        firefox_options.set_preference("pdfjs.disabled", True)
        firefox_options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        return self.driver
