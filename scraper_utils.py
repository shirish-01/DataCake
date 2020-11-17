import random
import re
from datetime import datetime,date

def time_stamper(delta='future',):
	def r(integer): return 1+random.randrange(integer)
	alphatime=datetime(2021+r(50), r(12), r(30), r(23),r(59),r(59))
	timestr=f'<time datetime="{alphatime}">Date: {alphatime}</time>'
	return timestr

def soup_select(soup,bs_select):
	try: return sanitize_text(soup.select_one(bs_select).prettify()) 
	except: return 'UNKNOWN'

def sanitize_text(text): 
	return re.sub(	r'\n|\t','',text)

		
def file_namer(text): 
	return "-".join(	re.sub(r'[\W]',' ',text).split()).lower()

def extract_body(mysoup):
	return str(mysoup.p.parent.extract())

def get_author_info(mysoup):
	authsoup=mysoup.find(class_=lambda x: x and 'author' in x)
	if not authsoup:
		return 'author unidentified'
	authorname=authsoup.findAll('a',text=True)[0].text
	authorlinks=[x['href'] for x in authsoup.findAll('a')]
	authdict={'name':authorname,'links':authorlinks}
	return authdict

# t=time_stamper()

# print(t)

# a='ASDCCxzczxccASDSAcXCzxczx'
