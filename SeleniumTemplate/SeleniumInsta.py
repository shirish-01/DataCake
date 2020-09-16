from selenium import webdriver as wd
from bs4 import BeautifulSoup as soup
import html5lib,requests,random,pyautogui,time,clipboard


def get_page_selenium(url,headless=True,strategy='eager'):
	opts = wd.firefox.options.Options()
	if headless: opts.headless = True 
	opts.page_load_strategy = strategy
	# opts.add_argument("--headless") #works standalone
	try:
		client 	= wd.Firefox(options=opts)
		client.get(url)
		markup= client.page_source
		client.quit()

		return markup

	except Exception as e:	client.quit();print("browser exit due to error"+str(e))


URL='https://pythonbasics.org/selenium-get-html/'
page=get_page_selenium(URL)
print(page)




