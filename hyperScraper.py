# V1.1
from mxproxy import mx
import threading, time
import os
import random
import re
from scraper_utils import *
	


class Memory:
	visitFileHomogenizeThreshold=100
	visitCount=1

class Logging:
	showDiscoverCount=0
	showPendingCount=0
	showCurrentVisit=1
		
class Explorer:
	'''USAGE:
			url='https://www.quicksprout.com'
			explorer=Explorer(url) 	#makes profiles and bg stuff
			startThreads(20,explorer.web_voyage)
	'''
	def __init__(self,url):
	#SEED VARIABLES
		self.url=url #same as input while initializing
		self.domain= url.split("/")[2] #==www.asdasd.com
		self.topLevelDomain=".".join(self.domain.split('.')[1:])
		self.baseurl='/'.join(url.split('/')[:3]) #==https://www.asdasd.com
		self.regex=self.baseurl+r'.*'
		print("LOG: regex url matching pattern is >>",self.regex)
	#INIT AND SETUP VARIABLES
		self.programName=	'hyperScraper'
		self.profileFolder=	self.programName+"_profiles/"
		self.currentDomainPath=	f'{self.profileFolder}/{self.domain}/'
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
		self.visitedURLMemory.add(current_visited_url) #never use set.update() for only 1 item

	def update_pendingURLMemory(self): #calculate after visiting
		self.pendingURLMemory= list(self.exploredURLMemory- self.visitedURLMemory)# ==A-B
		if Logging.showPendingCount: 
			print(len(self.exploredURLMemory)- len(self.visitedURLMemory),' |Pending URLSs')

	def get_all_links(self,soup): #unique set of link, adds discovered links to file
		freshlinks={l['href'] for l in soup.findAll('a',href=True)} ;#print(freshlinks)
		newlinksfiltered=set()
		for x in freshlinks: #FILTER UNWANTED LINKS
			# print('Track RAWURI',x)
			try:

				match=re.search(self.regex,x)
				if match: 
					matchtext=match.group()
					print("TRCKER regex ::",matchtext)
					newlinksfiltered.add(matchtext)
				if x[0]=='/' and ('http' not in x):#magic
					x=self.baseurl+x ; 
					# print('TX2:>>',x)

			except Exception as e:
				pass
				# print(e,x)
				# raise e

		return newlinksfiltered


	def visit(self,url): #visit page and gather info
		def extract_info(soup,url=url):
			pageDict={}
			pageDict['url']=url
			# print(soup.find('h1').text,'asdjhaskjdaskjdhaskjdhsd')
			pageDict['head']=sanitize_text(soup.find('h1').get_text())
			pageDict['body']=extract_body(soup)
			pageDict['time']=time_stamper(delta='future')
			pageDict['author']=get_author_info(soup)
			# return mx.jdumps(pageDict)
			return pageDict

		def save_to_disk(filename,data):
			mx.fwrite(self.domainDataFolder+f'{filename}.json',data)

		try:
			page= mx.get_page_soup(url)
			pageinfojson=extract_info(page)
			self.update_exploredURLMemory(self.get_all_links(page))
			self.update_visitedURLMemory(url)
			self.update_pendingURLMemory()
			save_to_disk(	file_namer(pageinfojson['head']) ,mx.jdumps(pageinfojson) )
			Memory.visitCount+=1
			if Logging.showCurrentVisit: 
				print(f'{ threading.current_thread().ident:<6}>> {url}')
		except Exception as e: 
			print('ERROR: while visiting >>',url,e)
			# raise e

	def web_voyage(self): #Recursive Crawling
		while self.pendingURLMemory:
			try:	
				url_current=mx.pickrandom(self.pendingURLMemory)
				self.visit(url_current)
				time.sleep(0.2)

			except Exception as e:
				# pass
				raise e
				print(e)
		print('>>> Voyage ENDED')

			# if len(os.listdir(self.domainDataFolder))>=2: #limit articles scraped
			# 	break


# DRIVER CODE
def startThreads(instance,count):
	threadBread=[]
	for c in range(count):
		thread= threading.Thread(target=instance.web_voyage)
		threadBread.append(thread)
		threadBread[c].start()
		time.sleep(0.5)

	'''||'''
	'''||'''
	'''||'''

	

#MAINCODE STARTS HERE
if __name__ == '__main__':
	urlinit='https://blog.hubspot.com/marketing/best-affiliate-programs'
	explorer=Explorer(urlinit)
	startThreads(explorer,13)

