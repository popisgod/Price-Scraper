
# Third party imports
import time 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException

CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
CHROMEDRIVER_PATH = 'chromedriver.exe'
GOOGLE_TRANSLATE = 'https://translate.google.com'


class Translator:
    def __init__(self, source : str = 'detect language', target : str = 'EN') -> None:
        # Intiate the selenium webdriver 
        options = Options()
        options.binary_location = CHROME_PATH
        options.add_argument('log-level=3')
        options.add_experimental_option("excludeSwitches", ['enable-logging'])
        options.add_experimental_option("detach", True)
        options.add_argument("--headless")
        self.webdriver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH),
                                    options=options)
        self.webdriver.get(GOOGLE_TRANSLATE)
        
        self.source = source
        self.target = target

        # ---- setting up the source language ----

        # BuiltIn timeout, waits until the condition has been fulfilled, returns the element
        try:
            WebDriverWait(self.webdriver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[1]/c-wiz/div[2]/button/div[3]'))).click()
        except TimeoutException as e:
            print('driver did not respond')
            raise e 
        
        # Type the language intended to be selected 
        language_selection_bar = self.webdriver.find_element(By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[1]/div/div[2]/input')
        language_selection_bar.send_keys(source)
        
        # Try to click the selected language 
        try: 
            WebDriverWait(self.webdriver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[1]/div/div[4]/div/div[1]'))).click()
        # In case the selected language doesn't exist catch error
        except ElementNotVisibleException as e:
            print('did not find source language')
            raise e 
        
        # ---- setting up the target language ----
        '''
        The problem is that some element, the details of which you removed from the error message, is in the way... on top of the element you are trying to click. 
        In many cases, this is some dialog or some other UI element that is in the way. 
        How to deal with this depends on the situation. If it's a dialog that is open, close it. 
        If it's a dialog that you closed but the code is running fast, wait for some UI element of the dialog to be invisible (dialog is closed and no longer visible) then attempt the click. 
        Generally it's just about reading the HTML of the element that is blocking, find it in the DOM, and figure out how to wait for it to disappear, etc.
        '''
        time.sleep(0.2)
        
        try:
            WebDriverWait(self.webdriver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[1]/c-wiz/div[5]/button/div[3]'))).click()
        except TimeoutException as e:
            print('driver did not respond')
            raise e 
        
        
        # Type the language intended to be selected 
        language_selection_bar = self.webdriver.find_element(By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[2]/div/div[2]/input')
        language_selection_bar.send_keys(target)
        
        time.sleep(0.25)
        
        # Try to click the selected language 
        try: 
             WebDriverWait(self.webdriver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[2]/div/div[4]/div/div[1]'))).click()
        # In case the selected language doesn't exist catch error
        except ElementNotVisibleException as e:
            print('did not find target language')
            raise e 
    
    def translate(self, text : str) -> str:
        """translates the received text 

        Args:
            text (str): text to be translated

        Returns:
            str: translated text 
        """
    
        try: 
            WebDriverWait(self.webdriver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea'))).send_keys(text)
        # In case the selected language doesn't exist catch error
        except ElementNotVisibleException as e:
            print('did not find target language')
            raise e 
        
        WebDriverWait(self.webdriver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[9]/div/div[4]/div[2]/span[2]/button/div[3]')))
        
        translated_text_element : WebElement =  WebDriverWait(self.webdriver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[9]/div/div[1]/span[1]/span/span')))
        
        translated_text = translated_text_element.text
        
        
        try: 
            WebDriverWait(self.webdriver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea'))).send_keys('test')
        # In case the selected language doesn't exist catch error
        except ElementNotVisibleException as e:
            print('did not find target language')
            raise e 
        
        WebDriverWait(self.webdriver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/div[1]/div/div[1]/span/button/div[3]'))).click()

        WebDriverWait(self.webdriver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[1]')))
        
        return translated_text

    
    def quit(self) -> None:
        self.webdriver.quit()

        
        
if __name__=='__main__':
    translator = Translator('EN', 'HE')
    print(translator.translate("hello, world"))
    