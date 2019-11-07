# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Launch():
    def __init__(self, code_snippet):
        self.code_snippet = code_snippet
        chromeoptions = Options()
        chromeoptions.add_argument('--no-sandbox')
        chromeoptions.headless = True
        self.driver = webdriver.Chrome(options=chromeoptions)
        self.driver.implicitly_wait(30)

    def action(self):
        driver = self.driver
        driver.get("https://sourceacademy.nus.edu.sg/playground")
        aceInputTextArea = driver.find_element_by_css_selector("textarea.ace_text-input")
        time.sleep(0.5)
        aceInputTextArea.clear()
        aceInputTextArea.send_keys(self.code_snippet)
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='play'])[1]/following::span[1]").click()
        parent_output = driver.find_element_by_css_selector("div.repl-output-parent")
        output = parent_output.find_element_by_css_selector("pre.bp3-code-block").text
        driver.quit()
        return output


