# V1.3
from mxproxy import mx
import threading, time
import os
import random
import re
	


class Memory:
	visitFileHomogenizeThreshold=100
	visitCount=1
	tempVisitCount=1
	beginTime=time.time()

class Processor:
	procpool='Pool()'

class Logging:
	showUrlPerSecond=1
	showVisitCount=1
	if showUrlPerSecond: showVisitCount=0 #cant coexist bcz of reset count required in url per second
	showCurrentVisit=0
	showPendingCount=0
	showDiscoverCount=0
		
class Explorer:
	'''USAGE:
			url='https://www.quicksprout.com'
			explorer=Explorer(url) 	#makes profiles and bg stuff
			startThreads(20,explorer.web_voyage)
	'''
	def __init__(self,url,myregex=r'/.*'):
	#SEED VARIABLES
		self.url=url #same as input while initializing
		self.domain= url.split("/")[2] #==www.asdasd.com
		self.topLevelDomain=".".join(self.domain.split('.')[1:])
		self.baseurl='/'.join(url.split('/')[:3]) #==https://www.asdasd.com
		self.regex=self.baseurl+myregex
		print("LOG: regex url matching pattern is >>",self.regex)
	#INIT AND SETUP VARIABLES
		self.programName=	'hyperScraper'
		self.profileFolder=	self.programName+"_profiles/"
		self.currentDomainPath=	self.profileFolder+f'{self.domain}/'
		self.domainDataFolder=	self.currentDomainPath+"data/"
		self.domainExploreFile=	self.currentDomainPath+'explored.url'
		self.domainVisitFile=	self.currentDomainPath+'visited.url'
		self.profile_check_make(self.domain) #MAKE A PROFILE FOR DOMAIN
	#INIT RUNTIME VARIABLES
		self.exploredURLMemory= mx.setload(	self.domainExploreFile	)
		self.visitedURLMemory=	mx.setload(	self.domainVisitFile	)
		self.pendingURLMemory= list(self.exploredURLMemory -self.visitedURLMemory)
		# self.sessionVisitCount=int(1)
	#INITIAL SEED
		try:
			self.visit(url)	#initialize seed url and build links
		except Exception as e:
			print("ERROR: initial Seed encountered serious error change to {raise e} in this line to track it")
			raise e

	def profile_check_make(self,domain): #smart profile management for scraper
		try: #make profile folder and create an domain
			os.makedirs(self.domainDataFolder)
			print('LOG: created path >>',self.domainDataFolder)
		except:
			print(f"WARNING: profile already exist for >> {self.domain}")
		finally:
			mx.touch(self.domainExploreFile) #Create if file not exist
			mx.touch(self.domainVisitFile)

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
		self.visitedURLMemory.add(current_visited_url) #never use set.update() for only 1 item

	def update_pendingURLMemory(self): #calculate after visiting
		self.pendingURLMemory= list(self.exploredURLMemory- self.visitedURLMemory)# ==A-B
		if Logging.showPendingCount: 
			print(f'PENDING URLS: {len(self.pendingURLMemory)}')

	def get_all_links(self,soup): #unique set of link, adds discovered links to file
		freshlinks={l['href'] for l in soup.findAll('a',href=True)} ;#print(freshlinks)
		newlinksfiltered=set()
		for x in freshlinks: #FILTER UNWANTED LINKS
			if not x:
				continue
			try:
				if x[0]=='/' and ('http' not in x):#magic
					x=self.baseurl+x ;
				if 'jpg' in x or 'png' in x:
					continue
				match=re.search(self.regex,x)
				if match: 
					matchtext=match.group()
					newlinksfiltered.add(matchtext)
			except Exception as e:
				raise e # DEPTH | 3
				pass 
		return newlinksfiltered


	def visit(self,url): #visit page and gather info
		import scraper_utils as su
		def extract_info(soup,url=url):
			[x.decompose() for x in soup.findAll(['script','head','style','iframe'])]#remove unwanted

			pageDict={}
			pageDict['url']=url
			pageDict['head']=	su.sanitize_text(soup.h1.text)
			pageDict['author']=	su.get_author_info(soup)
			pageDict['time']=	su.time_stamper(delta='future')
			pageDict['body']=	su.extract_body(soup)
			# return mx.jdumps(pageDict)
			return pageDict

		def save_to_disk(filename,data):
			mx.fwrite(self.domainDataFolder+f'{filename}.json',data)

		try:
			page= mx.get_page_soup(url) ; 
			if page == 404: return
			self.update_exploredURLMemory(self.get_all_links(page))
			self.update_visitedURLMemory(url)
			self.update_pendingURLMemory()
			pageDict=extract_info(page)
			save_to_disk( su.file_namer(pageDict['head']) ,mx.jdumps(pageDict) )
			Memory.visitCount+=1
			if Logging.showCurrentVisit: 
				print(f'WORKER VISIT >> {url}')
			if Logging.showVisitCount:
				print(f'SESSION VISITS | { Memory.visitCount }')
			if Logging.showUrlPerSecond:
				if int(time.time()) % 5 == 0:
					tdelta=time.time()-Memory.beginTime
					print('Pages-Per-Second : ',Memory.visitCount/tdelta)
		except Exception as e: 
			print('ERROR =',url,e)
			raise e # | DEPTH 2

	def web_voyage(self): #Recursive Crawling
		while self.pendingURLMemory:
			try:	
				url_current=mx.pickrandom(self.pendingURLMemory)
				self.visit(url_current)
				# time.sleep(random.random())
			except Exception as e:
				raise e # | DEPTH 1
		print('>>> Voyage ENDED')


# DRIVER CODE
def startThreads(instance,count):
	threadBread=[]
	print('Thread Parallelization Contract',count)
	for c in range(count):
		thread= threading.Thread(target=instance.web_voyage)
		threadBread.append(thread)
		threadBread[c].start()
		time.sleep(1)

	'''||'''
	'''||'''
	'''||'''

# ===================================>> MAINCODE STARTS HERE
if __name__ == '__main__':
	urlinit='https://www.quicksprout.com/blog/page/126/'
	explorer=Explorer(urlinit, myregex=r'/.*' )
	startThreads(explorer,30)

