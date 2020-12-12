import sys;success=0;importlevel="../";
for i in range(4): 
	if not success:
		try: sys.path.append(importlevel);from modulex import modulex as mx ;success=1;mx.cleanup();print("mx imported")
		except Exception as e: importlevel=importlevel + "../";

if __name__ == '__main__':
	url='https://stackoverflow.com/questions/125703/how-to-modify-a-text-file'
	page=mx.get_page(url, soupify=True)
	paras="\n".join(	list(map((lambda x:x.text),page.find_all('p'))) )
	print(paras)
