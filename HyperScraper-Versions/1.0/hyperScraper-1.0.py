'''
	VERSION: 1.0
	WORKING:
		The hyperScraper module clones the data on websites as we desire. by desire I mean that we can restructure data.
		the 'Explorer' class has various functions. when initialized with a url it creates a folder called hyperscraper_profiles
		which inturn is derived from current filename via __file__ global variable.

		once initialized it will create the domain name like www.example.com in profiles folder (which it just created). this is
		governed by the profile_check_make.

'''
from mxproxy import mx
import threading
import os
import random
	
class Memory:
	visitFileHomogenizeThreshold=10
	visitCount=1

class Macros:
	def homogenize(self,filename):
		threshold=Memory.visitFileHomogenizeThreshold
		if Memory.visitCount%threshold==0:
			iset=set(mx.fread(filename).split('\n'))
			uset="\n".join(list(iset))
			mx.fwrite(filename,uset)
			print('homogenized')

class Logging:
	showDiscoverCount=1
	showPendingCount=True
	showCurrentVisit=0
		
class Explorer:
	'''USAGE:
			url='https://www.quicksprout.com'
			explorer=Explorer(url) 	#makes profiles and bg stuff
			explorer.visit(url)	 	#initialize seed url
			startThreads(20,explorer.web_voyage)
	'''
	def __init__(self,url):
		self.url=url
		self.baseurl='/'.join(url.split('/')[0:3])
		self.domain= url.split("/")[2]
		self.pendingURLList=[]
		#dynamic profile creation variables
		self.programName=__file__.split("\\")[-1].split('.')[0]
		self.profileFolder=self.programName+"_profiles"
		self.currentDomainPath='./{}/{}/'.format(self.profileFolder,self.domain)
		self.domainDataFolder=self.currentDomainPath+"data/"
		self.domainExploreFile=self.currentDomainPath+'explored.url'
		self.domainVisitFile=self.currentDomainPath+'visited.url'
		self.profile_check_make(self.domain) #MAKE A PROFILE FOR DOMAIN


	def profile_check_make(self,domain):
		#smart profile management for scraper
		try:
			#make profile folder and create an domain
			if not os.path.exists(self.profileFolder): 
				os.mkdir(self.profileFolder) ;print("Created Folder",self.profileFolder)
			os.mkdir(self.currentDomainPath)

			if not os.path.exists(self.domainDataFolder):
				os.mkdir(self.domainDataFolder)

		except:
			print(self.domain,"profile already exist")
		finally:
			mx.touch(self.domainExploreFile) #Create if file not exist
			mx.touch(self.domainVisitFile) #Create if file not exist

	# ============================MAIN LOGIC FUNCTONS==============================

	def explore_links_on_page(self,soup):
		#unique set of link, adds discovered links to file
		def update_exploredURLMemory(self,nowDiscovered):
			self.exploredURLMemory= set(mx.fread(self.domainExploreFile).split('\n'))#reducing compute
			difference= list(set(nowDiscovered).difference(self.exploredURLMemory))
			self.exploredURLMemory.update(difference)
			updateFile= mx.fappend(self.domainExploreFile, "\n".join(difference+['\n']))
			if Logging.showDiscoverCount: 
				print(f"added {len(difference)} URL records\n")


		allLinks=soup.findAll('a',href=True)
		filteredLinks=[l['href'] for l in allLinks if ('-' or 'html' in l['href']) or (l['href'][0]=='/')  ]
		# filteredLinks=[ul for ul in filteredLinks ] #Relative url Handling
		filteredLinks=[x for x in filteredLinks if ('http' in x) and (self.baseurl == x[:len(self.baseurl)]) and ('comment' not in x)]
		update_exploredURLMemory(self,filteredLinks)
		self.calculate_pending_url_list(url)


	def calculate_pending_url_list(self,nowVisited):#calculate after visiting
		def update_visitedURLMemory(nowVisited):
			#update in file First Important
			Macros.homogenize(self,self.domainVisitFile)
			mx.fappend(self.domainVisitFile,"\n"+nowVisited)
			self.visitedURLMemory=mx.fread(self.domainVisitFile).split('\n')
		#||
		update_visitedURLMemory(nowVisited)
		self.pendingURLList=list(self.exploredURLMemory.difference(self.visitedURLMemory))# ==A-B


	#visit page and gather info
	def visit(self,url,save=1):
		def extract_info(soup):
			p=[x.e for x in soup.findAll(['script','style'])]
			currentPageData={}
			headtags= ['h1','h2','h3','h4']
			currentPageData['url']= url
			currentPageData['headings']= {h:[x.text for x in soup.findAll(h) if x.text!='' ] for h in headtags}
			currentPageData['images']= [x['src'] for x in soup.findAll('img') if len(x['src'])<500 ]
			currentPageData['content']=[(lambda x:x.text)(x.extract())  for x in soup.findAll('p') ]
			return mx.jdumps(currentPageData)

		def save_to_disk(label,data):
			mx.fappend(self.domainDataFolder+f'{label}.json',data)

		try:
			mx.get_page=mx.get_page_soup
			page= mx.get_page(url)
			self.explore_links_on_page(page)
			self.calculate_pending_url_list(url)
			if save : save_to_disk(extract_info(page))
			Memory.visitCount+=1		
		except Exception as e:
			print('exception during visit:',e)

	#Recursive Crawling
	def web_voyage(self):
		# self.visit(self.url)
		for e in self.pendingURLList:
			choice= random.choice(self.pendingURLList)
			self.pendingURLList.remove(choice)
			self.visit(choice)
			if Logging.showCurrentVisit: print('current :',choice)
			if Logging.showPendingCount: print(len(explorer.pendingURLList),'pending URLs')



# DRIVER CODE
def startThreads(count,functionInstance,argsTuple=''):
	threadBread=[]
	for thread in range(count):
		thread= threading.Thread(target=functionInstance, args=() )#can use eval for args tuple
		threadBread.append(thread)
	for thread in threadBread:
		thread.start()

if __name__ == '__main__':
	url='https://www.quicksprout.com'
	explorer=Explorer(url)
	explorer.visit(url)#initialize seed url
	startThreads(20,explorer.web_voyage)


	
	# d=mx.fread('C:\\Users\\dell\\Documents\\GitHub\\DataCake\\hyperScraper_profiles\\www.labnol.org\\data\\data-chunk-1.json')
	# print(d[:100000])
