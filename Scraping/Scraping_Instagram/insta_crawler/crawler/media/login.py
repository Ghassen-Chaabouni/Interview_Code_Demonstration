from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
import time

class Login:
	def __init__(self, driver, username, password):
		self.driver = driver
		self.username = username
		self.password = password
	def signin(self):
		flag = False
		while(not flag):
			self.driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
			uid = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '._2hvTZ.pexuQ.zyHYP')))
			uid.click()
			uid.send_keys(self.username)
			pswd = self.driver.find_elements_by_css_selector('._2hvTZ.pexuQ.zyHYP')[1]
			pswd.click()
			pswd.send_keys(self.password)
			btn = self.driver.find_element_by_css_selector('.sqdOP.L3NKy.y3zKF')
			btn.click()
			time.sleep(5)
			flag= True

		return self.driver 
			



