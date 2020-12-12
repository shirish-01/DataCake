import random
import re

def time_stamper(delta='future',):
	from datetime import datetime,date
	def r(integer): return 1+random.randrange(integer)
	try:
		alphatime=datetime(2021+r(50), r(12), r(29), r(23),r(59),r(59))
	except Exception as e:
		alphatime=datetime(2021+r(50), r(12), r(29), r(23),r(59),r(59))
	timestr=f'<time datetime="{alphatime}">Date: {alphatime}</time>'
	return timestr

def sanitize_text(text): 
	return re.sub(	r'\n|\t','',text)

def file_namer(text): 
	return "-".join(	re.sub(r'[\W]',' ',text).split()).lower()

def extract_body(mysoup):
	# NOTE: extract body is a heavy function and is destructive
	# so on every iteration a tag is removed from tree which might have some other info.
	# recommended to call this at last while extracting info from page
	parafind=mysoup.findAll('p')
	lastParentLen=0; theRealParent=[]
	try:
		while mysoup.find('p'):
			parent=mysoup.find('p').parent.extract()
			if lastParentLen<len(parent):
				theRealParent=parent
				lastParentLen=len(parent)
		if len(theRealParent)<10: #body too short handling
			return  theRealParent.text
		return str(theRealParent).replace('\n','<br>')
	except Exception as e:
		pass

def get_author_info(mysoup):
	def r(k=24):
		return "".join(random.choices(list('1234567890abcdef'),k=24))
	authorgrav=f'https://www.gravatar.com/avatar/{r()}?s=32&d=identicon&r=PG'
	authsoup=mysoup.find(class_=lambda x: x and 'author' in x)
	if not authsoup: 
		return {'name':r(), 'image':authorgrav, 'links':''}

	authorlinks=list({x['href'] for x in authsoup.findAll('a',href=True)})
	try:
		authorname=authsoup.findAll('a',text=True)[0].text
	except:
		authorname= r()
	authdict={
		'name':authorname,
		'image':authorgrav,
		'links':authorlinks}
	return authdict


if __name__ == '__main__' :
	print('running as main')
	pass