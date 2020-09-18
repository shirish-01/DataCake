from mxproxy import mx
import os

class Memory:
	def __init__(self,domainExploreFile):
		self.domainExploreFile=domainExploreFile

	def get_explored_links(self,domainExploreFile):
		return set(mx.fread(domainExploreFile).split('\n'))

	def set_explored_links(self,domainExploreFile,newLinks):
		nowDiscovered= 	set(nowDiscovered)
		prevDiscovered= set(mx.fread(self.domainExploreFile).split('\n'))
		difference= 	list(nowDiscovered-prevDiscovered)
		mx.fappend(self.domainExploreFile, "\n".join(difference))
		union= 			prevDiscovered.union(nowDiscovered)
		print("added {} URL records".format(len(difference)))
		
class Explorer:

	def __init__(self,url):
		self.url=url
		self.baseurl='/'.join(url.split('/')[0:3])
		self.domain= url.split("/")[2]

		#dynamic profile creation variables
		self.programName=__file__.split("\\")[-1].split('.')[0]
		self.profileFolder=self.programName+"_profiles"
		self.currentDomainPath='./{}/{}/'.format(self.profileFolder,self.domain)
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
		except:
			print(self.domain,"profile already exist")
		finally:
			mx.touch(self.domainExploreFile) #Create if file not exist
			mx.touch(self.domainVisitFile) #Create if file not exist

	def update_explore(self,nowDiscovered):
		#unique set of link knowledge
		nowDiscovered= 	set(nowDiscovered)
		prevDiscovered= set(mx.fread(self.domainExploreFile).split('\n'))
		difference= 	list(nowDiscovered-prevDiscovered)
		mx.fappend(self.domainExploreFile, "\n".join(difference))
		print("added {} URL records".format(len(difference)))

		fullUrlRecords=	prevDiscovered.union(nowDiscovered)
		return fullUrlRecords

	def findLinks(self,url):
		page=mx.get_page(url, soupify=True)
		allLinks=page.findAll('a',href=True)
		filteredLinks=[l['href'] for l in allLinks if ('-' or 'html' in l['href']) or (l['href'][0]=='/')  ]
		self.update_explore(filteredLinks)
		# print(filteredLinks)

	def voyage():
		pass
	def urlPhilter(self,urlSet,include):
		pass



# DRIVER CODE
if __name__ == '__main__':
	# homeurl="https://www.livemint.com/companies/start-ups"
	url='https://www.shoutmeloud.com/blog'
	explorer=Explorer(url)

	testx=explorer.findLinks(url)




