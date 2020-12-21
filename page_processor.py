# UPPER LEVEL API
import auto_dict
import auto_syn
import random,re,os
from mxproxy import mx
Cache=mx.Cache


class Page:
	'''docstring'''
	def __init__(self,string):
		self.string=self.remove_comments(string)
		self.soup=mx.make_soup(self.string)
		self.text=self.soup.text
		self.cleaned=''
		self.bsoup=''
		self.hardwords=''

	def remove_comments(self,string):
		return re.sub(r'<!.*?->','', string) 

	def preserve_only_href_src(self):
		for x in self.soup.findAll():
			if x.name not in ['a','img']:
				del x.attrs
		return self

	def remove_empty(self,bsoup):
		for x in bsoup.findAll():
			if not x.text:
				print(x.text)
				x.decompose()
		return bsoup

	def get_hardwords(self,string,threshold=6):
		result=set(re.findall(r'[\w]*',string))
		result={x for x in result if len(x)>=threshold }
		return result

def get_random_article():
	navdir='hyperScraper_profiles/'
	randomDomain=navdir+mx.pickrandom(os.listdir(navdir))+'/data/'
	if os.listdir(randomDomain):
		randomPage	=randomDomain+random.choice(os.listdir(randomDomain))
		pagedict=mx.jload(randomPage)
		pagedict['localpath']=randomPage
		return pagedict
	else:
		get_random_article()

if __name__ == '__main__':
	# randomArticle=get_random_article()
	seededArticle=mx.jload('sample_page.json')

	myPage=Page(seededArticle['body'])
	text=myPage.soup.findAll('p')[:8]
	for p in text:
		print(p)
		print(p.string,'\n')
