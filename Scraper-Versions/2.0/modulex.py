#================= IO RELATED
import os
import sys
def fread(path):
	f=open(path,'r+',).read()
	return f

def setload(path,seperator='\n'):
	return set(fread(path).split(seperator))

def fwrite(fname,content):
	f=open(fname,"w+",errors="ignore")
	f.write(content)

def fappend(fname,content):
	f=open(fname,"a+",errors="ignore")
	f.write(content)

def touch(fpath):
	check= os.path.exists(fpath)
	(lambda fname1:[open(fname1,"w+",errors="ignore").write(""),print('Touched',fname1)] 
		if not check else None) (fpath)

def softwrite(fname,content):
	f=open(fname,"w+").write(content) if not os.path.exists(fname)	else print('file exists, ricsk nai lene ka')

def cleanup():
	import shutil
	try: shutil.rmtree('__pycache__')
	except :pass
cleanup()


#DATA FUNCTIONS
def pickrandom(L):
	i = random.randrange(len(L)) # get random index
	L[i], L[-1] = L[-1], L[i]    # swap with the last element
	return L.pop()                  # pop last element O(1)


# =============== AUTO_PACKAGE
def auto_pip(mode,modulesList):
	'''
		+DOC: automatically Install Pip Packages Without Missing Module 
		Error before code runs and upgrades pip if its old, failsafe and fast
		can be invoked within code rather than running pip install blah 
		from cmd/terminal.
		+USAGE: auto_pip('mode',[modules])
				auto_pip('install',['pytorch','numpy','etc...']) 
		where mode can be {install,uninstall,download} and modules is
		a standard py list ['numpy','pandas','tensorflow==1.15.1' and so on...]
		+NOTES: downloading can be useful if want to install later 
		from local source and avoid network cost.
	'''
	import subprocess as sp
	#>>> preflight check && upgrade if old
	proc=sp.run('pip list',stdout=sp.PIPE,stderr=sp.PIPE,text=1)
	if 'You should consider upgrading' in proc.stderr:
		upgradeCommand=proc.stderr.split('\'')
		sp.run(upgradeCommand[1])

	pipInstallSignal,pipUninstallSignal= 0,0 #declare signals as 0,
	#below dict-> true if module present against module name ex: numpy:True
	satisfied={x:(x in proc.stdout) for x in modulesList} 
	for k,v in satisfied.items():
		print(k+'\t:preinstalled') if v else print(k,'is missing',end=' =|= ')
		if v==False: pipInstallSignal=1  
		if v==True: pipUninstallSignal=1 #NAND Condition if true then start uninstalling
	
	if mode=='download':
		proc=sp.run(f'pip download {" ".join(modulesList)} ' ,stdout=sp.PIPE	,shell=0)
		output=proc.stdout.read().decode('ascii').split('\n')
		print([x for x in output if 'Successfully' in x][0])
		proc.kill()
			
	if mode=='install': 
		if pipInstallSignal==True: 
			proc=sp.run('pip install {} -U'.format(" ".join(modulesList)),text=True,shell=1)
		else: print(f'\n{modulesList} were already installed'); return 1 

	if mode=='uninstall': 
		if pipUninstallSignal==True: 
			proc=sp.run('pip uninstall -y {}'.format(" ".join(modulesList)),text=True,shell=0)
		else: print(f'\n{modulesList} were already uninstalled'); return 1

	#CHECK SUCCESS OF PROCESS
	if proc.returncode==0:
		print('auto_pip Run Success')
		return proc.returncode




# =============== Miscalleneous
def kill_code():
	''' immediately kill running code regardless prority of current code'''
	import os
	os.kill(os.getpid(),signal.SIGABRT)
kill_switch=kill_code






# ===============JSON FUNCTIONS
import json
def jloads(string): #return dict
	return json.loads(string)
def jload(fromfile): #return dict
	return json.load(open(fromfile))

def jdumps(dictonary): #return string
	return json.dumps(dictonary,indent=4)
def jdump(dictonary,toFile): #write to disk
	return json.dump(dictonary,open(toFile,"w+"),indent=4)






#=============== PARALLELISM
import threading
def threadQueue(workQueue,worker):
	pass

def parallelFunction(functionVariableName,threadCount):
	''' BEST USED FOR INTERNET ATTACKS OR REPETITIVE TASKS'''
	import threading
	pool=[]
	for i in range(threadCount):
		thread=threading.Thread(name='parallelFunction', target=functionVariableName)
		pool.append(thread)
		pool[i].start()
threadMaker=parallelFunction



#===============WEB FUNCTIONS
import html5lib,requests
from bs4 import BeautifulSoup as soup
try:
	import cchardet as chardet
except Exception as e:
	pass
requestPool=[requests.Session() for x in range(5)]
def get_page_soup(url,makesoup=True):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
	randSession=random.choice(requestPool) #pick a random session for reducing traffic to single connection
	req=randSession.get(url,headers=headers,timeout=10)
	if req.status_code==404:
		return 404
	if makesoup==True :
		return soup(req.text,'html.parser')


def get_page_selenium(url,headless=True,strategy='normal'):
	from selenium import webdriver as wd
	opts = wd.firefox.options.Options();	
	opts.page_load_strategy = strategy
	if headless: opts.headless = True 
	# opts.add_argument("--headless") 		#works standalone
	try:
		client 	= wd.Firefox(options=opts);
		client.get(url);
		markup= client.page_source;
		return client,markup
	except Exception as e:	client.quit();	print("browser exit due to error"+str(e))

def push_tab(client,url):
	client.execute_script("window.open('{}', '_blank')".format(url))






#______________________________________________
#@#$%@#$%#$%#$%#+++CRYPTOGRAPHY+++#@$#@$#@$!@# 
import random
class Swamicrypt:
	'''	usage 
		passwd=Swamicrypt('password')
		print(passwd.credentials)
	'''
	def __init__(self, basepassword):
		self.basepassword= basepassword
		self.cryptSpace= self.generate_alphanumeric_chars()
		self.storage= self.cryptx()
		self.credentials= self.make_key(self.storage[0],self.storage[1])
# 
	def generate_alphanumeric_chars(self):
		rn=range
		space=  [chr(x) for x in rn(ord("0"),ord("9")+1)]
		space+= [chr(x) for x in rn(ord("a"),ord("z")+1)]
		space+= [chr(x) for x in rn(ord("A"),ord("Z")+1)]
		return space
# 
	def cryptx(self,security=4):
		def r(namespace,k=security): return random.sample(namespace,k=k)
		cryptSpace=self.cryptSpace
		keySpace=[r(cryptSpace,k=1)[0] for x in range(len(self.basepassword)*security)]
		keySpace="".join(keySpace)
		return (self.basepassword,keySpace)

	def make_key(self,stringx,keySpace):
		ks_indices=random.sample(list(enumerate(keySpace)) ,k=len(stringx))
		ord_add=[ord(s)+ord(p[1]) for s,p in zip(stringx,ks_indices)]
		key=[str(ki[0])+'+'+str(oa) for ki,oa in zip(ks_indices,ord_add)]
		key='.'.join(key)
		return key,keySpace

	def decryptx(self,credentials):
		key,keyspace=credentials
		key=key.split('.')
		imods=[x.split('+') for x in key]
		orignalPassword=[ chr(int(x[1]) - ord(keyspace[int(x[0])])) for x in imods ]
		return "".join(orignalPassword)

if __name__ == '__main__':
	import random,re
	# from nltk.corpus import stopwords
	# nltk_stopwords = set(stopwords.words('english'))
	# print(nltk_stopwords)

	import spacy
	sp = spacy.load('en_core_web_sm')
	spacy_stopwords = sp.Defaults.stop_words


	url='https://backlinko.com/google-ranking-factors#brand'
	url='http://www.hubspot.com/resources/'
	page=get_page_soup(url)

