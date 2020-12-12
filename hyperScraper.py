# V1.3
'''USAGE:
		url='https://www.quicksprout.com'
		explorer=Explorer(url) 	#makes profiles and bg stuff
		startThreads(20,explorer.web_voyage)
'''

import multiprocessing
import threading, time
import os
import random
import re
import scraper_utils as su
from bs4 import BeautifulSoup as soup
from mxproxy import mx

class Processor:
	def save_page_info(self,markup,url): # multiprocessing supported function
		def extract_info(soup,url='not assigned'):#indirect function
			[x.decompose() for x in soup.findAll(['script','head','style'])]#remove unwanted
			pageDict={} ; pageDict['url']=url
			pageDict['head']=	su.sanitize_text(soup.h1.text)# if no head in url page is probably waste
			pageDict['author']=	su.get_author_info(soup)
			pageDict['time']=	su.time_stamper(delta='future')
			pageDict['body']=	su.extract_body(soup)
			return pageDict
			...
		def write_to_disk(self,filename,data):
			mx.fwrite(self.domainDataFolder+f'{filename}.json',data)
			...
		try:		
			mysoup=soup(markup,features='html.parser')
			pageDict=extract_info(mysoup,url=url)
			write_to_disk(self, su.file_namer(pageDict['head']) ,mx.jdumps(pageDict) )
			...
		except Exception as e:
			print(e,url)


class Memory: 
	visitCount=1 ; beginTime=time.time()+5


class Logging:
	showUrlPerSecond=1
	showVisitCount=0
	showCurrentVisit=0
	showPendingCount=0
	showDiscoverCount=0
	def calculate_url_second():
		if Memory.visitCount % 5 == 0:
			tdelta=time.time()-Memory.beginTime
			print('Pages-Per-Second : ',Memory.visitCount/tdelta)



class Explorer:
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
		if Logging.showDiscoverCount: 
			print(f"Discovered {len(difference)} URLS")
		difference= newLinks - self.exploredURLMemory #save DATA IO by calc difference
		if difference:
			mx.fappend(self.domainExploreFile, "\n".join(difference)+'\n')
			self.exploredURLMemory.update(newLinks) #add just discovered links

	def update_visitedURLMemory(self,current_visited_url):
		if Logging.showCurrentVisit: 	
			print(f'WORKER VISIT >> {current_visited_url}')
		if current_visited_url not in self.visitedURLMemory: 
			mx.fappend(self.domainVisitFile,"\n"+current_visited_url)
		self.visitedURLMemory.add(current_visited_url) #never use set.update() for only 1 item

	def update_pendingURLMemory(self): #calculate after visiting
		if Logging.showPendingCount: print(f'PENDING URLS: {len(self.pendingURLMemory)}')
		self.pendingURLMemory= list(self.exploredURLMemory- self.visitedURLMemory)# ==A-B

	def get_all_links(self,soup): #unique set of link, adds discovered links to file
		freshlinks={l['href'] for l in soup.findAll('a',href=True)} ;#print(freshlinks)
		newlinksfiltered=set()
		for x in freshlinks: #FILTER UNWANTED LINKS
			if not x:
				continue
			try:
				if x[0]=='/' and ('http' not in x):#works like magic
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
		try:
			page_req= mx.get_page(url) #requests.get object
			if page_req.status_code != 200 : #break if page error
				mx.fappend(self.currentDomainPath+'errors.url', 	f'\nPAGE ERROR :{page_req.status_code,url}' ); return

			page_text=page_req.text #page text cache
			Pool.apply(Processor.save_page_info, (self,page_text,url)) #asyncProcessing using Processor Module
			soup=mx.soup(page_text,features='html.parser')
			self.update_exploredURLMemory(self.get_all_links(soup)) #1
			self.update_visitedURLMemory(url) #2
			self.update_pendingURLMemory() #3 dont change order
			Memory.visitCount+=1
			if Logging.showVisitCount: 		print(f'SESSION VISITS | { Memory.visitCount }')
			if Logging.showUrlPerSecond:	Logging.calculate_url_second()
				
		except Exception as e: 
			print('ERROR =',url,e)
			raise e # | DEPTH 2

	def web_voyage(self): #Recursive Crawling
		while self.pendingURLMemory:
			try:	
				url_current=mx.pickrandom(self.pendingURLMemory)
				self.visit(url_current)
			except Exception as e:
				raise e # | DEPTH 1
		print('>>> Voyage ENDED')



#==============================================	MAINCODE STARTS HERE
if __name__ == '__main__':
	Pool=multiprocessing.Pool(8)

	# DRIVER CODE
	def startThreads(instance,count):
		threadBread=[]
		print('Thread Parallelization Contract',count)
		[threading.Thread(target=instance.web_voyage).start() for x in range(count)]

		for c in range(count):
			thread= threading.Thread(target=instance.web_voyage)
			threadBread.append(thread)
			threadBread[c].start()
			time.sleep(0.2)

	urlinit='https://www.shoutmeloud.com/'
	explorer=Explorer(urlinit, myregex=r'/.*' )
	startThreads(explorer,20)

