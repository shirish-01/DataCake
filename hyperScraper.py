from mxproxy import mx
import os


 
class Explorer:

	def __init__(self,url):
		self.url=url
		self.domain= url.split("/")[2]
		self.domainCategory= url.split("/")[-1] #https://..asd/(category)<-

	def profile_check_make(self,entity):
		#smart profile management for scraper
		programName=__file__.split("\\")[-1].split('.')[0]
		profileFolder=programName+"_profiles"
		currentEntityPath='./{}/{}/'.format(profileFolder,entity)
		entityExploreFile=currentEntityPath+'explored.url'
		entityVisitFile=currentEntityPath+'visited.url'

		try:
			#make profile folder and create an entity
			if not os.path.exists(profileFolder): 
				os.mkdir(profileFolder) ;print("Created Folder",profileFolder)
			os.mkdir(currentEntityPath)
		except:
			print(self.domain,"profile already exist")
		finally:
			mx.touch(entityExploreFile) #Create if file not exist
			mx.touch(entityVisitFile) #Create if file not exist
			# print("Touched =>",[entityExploreFile,entityVisitFile])

	def explore(self):
		self.page = 	 mx.get_page(self.url,soupify=True)
		self.page.urls = [x['href'] for x in self.page.find_all(href=True)]

		#load in memory if exist
		goodUrl=set(filter(lambda x:'.html' and self.domainCategory in x,self.page.urls))
		self.profile_check_make(self.domain)






	def update_explore():
		pass

	def update_visit():
		pass

# DRIVER CODE
if __name__ == '__main__':
	homeurl="https://www.livemint.com/companies/start-ups"
	explorer=Explorer(homeurl)
	explorer.explore()


	# pno=1
	# pagesExhausted=0
	# while pagesExhausted != 1 and pno <3:
	# 	try:
	# 		dynlink=baseurl+"/page-{}".format(pno)
	# 		spider=Spider(baseurl)
	# 		goodUrl=set(filter(lambda x:'.html' and category in x,spider.page.urls))
	# 		print(len(goodUrl))

	# 		pno+=1
	# 	except Exception as e:
	# 		pagesExhausted=1
	# 		print(category,"Exhaust @ page{} with error {}".format(pno-1,e))





