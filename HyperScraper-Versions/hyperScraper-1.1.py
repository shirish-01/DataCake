'''
	VERSION: 1.1
	WHATS NEW:
		+added regex module, change the regex condition in Explorer class > self.regex . we can put rules like
		for example 
		url given as 'https://www.entrepreneur.com/article/35949'
		baseurl becomes https://www.entrepreneur.com/
		self.regex= self.baseurl+r'/article.*' 
		self.regex 	now equal to 'https://www.entrepreneur.com/.*'

		+added sanitize text option to remove junk characters like \n \t etc, it can
		be customized in sanitize_text function, re.sub is used.

		+enhanced the initialization of Explorer class, now it automatically makes a profile 
		and calculate explored and visited links when new url is inputted and does not 
		require to kickstart it twice to get going.

		+removed homogenizing of files function at regular intervals ie remove duplicate
		url entries, now the update{explored,visited}URLMemory functions only differentially
		add new links and save harddisk i/o

		+organized update_exploredURLMemory, update_visitedURLMemory, update_pendingURLMemory 
		to make process atomic and gain more precision and easier debugging. nesting them in
		previous versions were very buggy and tracing errors was very difficult.

		+Explorer.get_all_links() the regex condition is applied here, modifythe function if
		your requirements to filter links are different.
				

'''
from mxproxy import mx
import threading, time
import os
import random
import re
	
def sanitize_text(text):
	return re.sub(r'\n|\t','',text)

class Memory:
	visitFileHomogenizeThreshold=100
	visitCount=1

class Logging:
	showDiscoverCount=0
	showPendingCount=1
	showCurrentVisit=0
		
class Explorer:
	'''USAGE:
			url='https://www.quicksprout.com'
			explorer=Explorer(url) 	#makes profiles and bg stuff
			explorer.visit(url)	 	#initialize seed url
			startThreads(20,explorer.web_voyage)
	'''
	def __init__(self,url):
		#SEED VARIABLES
		self.url=url
		self.baseurl='/'.join(url.split('/')[0:3])
		self.domain= url.split("/")[2]
		self.regex=self.baseurl+r'/article.*'
		print(self.regex)


		#INIT AND SETUP VARIABLES
		self.programName='hyperScraper'
		self.profileFolder=self.programName+"_profiles"
		self.currentDomainPath='./{}/{}/'.format(self.profileFolder,self.domain)
		self.domainDataFolder=self.currentDomainPath+"data/"
		self.domainExploreFile=self.currentDomainPath+'explored.url'
		self.domainVisitFile=self.currentDomainPath+'visited.url'
		self.profile_check_make(self.domain) #MAKE A PROFILE FOR DOMAIN

		#RUNTIME VARIABLES
		self.exploredURLMemory= mx.setload(	self.domainExploreFile	)
		self.visitedURLMemory=	mx.setload(	self.domainVisitFile	)
		self.pendingURLMemory= list(self.exploredURLMemory -self.visitedURLMemory)

		#INITIAL SEED
		self.visit(url)	#initialize seed url and build links

	def profile_check_make(self,domain):
		#smart profile management for scraper
		try:
			#make profile folder and create an domain
			if not os.path.exists(self.profileFolder): 
				os.mkdir(self.profileFolder)
			if not os.path.exists(self.currentDomainPath):
				os.mkdir(self.currentDomainPath)
			if not os.path.exists(self.domainDataFolder):
				os.mkdir(self.domainDataFolder)
		except:
			print(self.domain,"profile already exist")
		finally:
			mx.touch(self.domainExploreFile) #Create if file not exist
			mx.touch(self.domainVisitFile) #Create if file not exist

	# ============================MAIN LOGIC FUNCTONS==============================

	def update_exploredURLMemory(self,newLinks):
		difference= newLinks - self.exploredURLMemory #save DATA IO by calc difference
		if difference:
			mx.fappend(self.domainExploreFile, "\n".join(difference)+'\n')
			self.exploredURLMemory.update(newLinks) #add just discovered links
		if Logging.showDiscoverCount: print(f"Discovered {len(difference)} URLS")

	def update_visitedURLMemory(self,current_visited_url):
		if current_visited_url not in self.visitedURLMemory:
			mx.fappend(self.domainVisitFile,"\n"+current_visited_url)
		self.visitedURLMemory.add(current_visited_url)

	def update_pendingURLMemory(self):#calculate after visiting
		self.pendingURLMemory= list(self.exploredURLMemory- self.visitedURLMemory)# ==A-B
		if Logging.showPendingCount: print(len(self.exploredURLMemory)- len(self.visitedURLMemory),' == pending Count')

	def get_all_links(self,soup):
		#unique set of link, adds discovered links to file
		freshlinks=[l['href'] for l in soup.findAll('a',href=True)]
		newlinksfiltered=set()
		for x in freshlinks: #FILTER UNWANTED LINKS
			if x[0]=='/':
				x=self.baseurl+x # print(x)
			match=re.search(self.regex,x)
			if match: 
				matchtext=match.group()
				newlinksfiltered.add(matchtext)
		# print(newlinksfiltered)
		return newlinksfiltered


	def visit(self,url): #visit page and gather info
		def extract_info(soup,url=url):
			def soup_select(soup,bs_select):
				try: return sanitize_text(soup.select_one(bs_select).text) 
				except: return 'UNKNOWN'

			bodyIdentifier='article'
			headIdentifier='h1'
			pageDict={}
			pageDict['url']=url
			pageDict['head']=soup_select(soup,headIdentifier)
			pageDict['body']=soup_select(soup,bodyIdentifier)
			pageDict['time']=str(random.randint(1,90)/2)+'Days Ago'
			pageDict['imgs']=str(soup.select(bodyIdentifier+' img'))
			# return mx.jdumps(pageDict)
			return pageDict

		def save_to_disk(label,data):
			mx.fwrite(self.domainDataFolder+f'{label}.json',data)
		Macros.homogenize(self,self.domainVisitFile)#remove duplicate entries in file

		try:
			page= mx.get_page_soup(url)
			pageinfojson=extract_info(page)
			self.update_exploredURLMemory(self.get_all_links(page))
			self.update_visitedURLMemory(url)
			self.update_pendingURLMemory()
			save_to_disk(	pageinfojson['head'].lower() ,mx.jdumps(pageinfojson) )
			Memory.visitCount+=1
			if Logging.showCurrentVisit: print(f'{ threading.current_thread().ident:<6}>> {url}')
		except Exception as e: print('exception 		',url,e)

	def web_voyage(self): #Recursive Crawling
		# self.update_pendingURLMemory()
		while True:
			url_current=mx.pickrandom(self.pendingURLMemory)
			self.visit(url_current)
			time.sleep(0.2)
		print('>>> Voyage ENDED')



# DRIVER CODE
def startThreads(instance,count):
	threadBread=[]
	for c in range(count):
		thread= threading.Thread(target=instance.web_voyage)
		threadBread.append(thread)
		threadBread[c].start()
		time.sleep(0.5)





#MAINCODE STARTS HERE
if __name__ == '__main__':
	urlinit='https://www.entrepreneur.com/article/359493'
	explorer=Explorer(urlinit)
	startThreads(explorer,20)

