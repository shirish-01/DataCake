from mxproxy import mx

class Logic:
	def __init__(self):
		pass	

	def filter(stringlist,include):
	# inclusive filter stringlist intersection include
		return list(filter(lambda x: True if include in x else False,stringlist))

	def get_hrefs(soupList): 
	#error proof href extraction from anchor tags
		l=[]
		try:
			for a in anchors: l.append(a['href'])
		except Exception as e: pass
		return l

class memory:
	"""docstring for memory"""
	def __init__(self, arg):
		super(memory, self).__init__()
		self.arg = arg
		
 
class Spider:
	def __init__(self,url):
		self.page = 	 mx.get_page(url,soupify=True)
		self.page.urls = [x['href'] for x in self.page.find_all(href=True)]
	
	def explore():
		pass
	
	def extract_data(url):
		return	mx.get_page_selenium(url,strategy="normal")

	def update_explore():
		pass

	def update_visit():
		pass







# DRIVER CODE
if __name__ == '__main__':
	baseurl="https://www.livemint.com/companies/start-ups"
	category=baseurl.split("/")[-1]

	pno=1
	pagesExhausted=0
	while pagesExhausted != 1 and pno <3:
		try:
			dynlink=baseurl+"/page-{}".format(pno)
			spider=Spider(baseurl)
			goodUrl=set(filter(lambda x:'.html' and category in x,spider.page.urls))
			print(len(goodUrl))

			pno+=1
		except Exception as e:
			pagesExhausted=1
			print(category,"Exhaust @ page{} with error {}".format(pno-1,e))


