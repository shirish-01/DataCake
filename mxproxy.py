import sys;success=0;importlevel="../";
for i in range(4): 
	if not success:
		try: sys.path.append(importlevel);from modulex import modulex as mx ;print("mx imported");success=1;mx.cleanup()
		except Exception as e: importlevel=importlevel + "../"

if __name__ == '__main__':
	page=mx.get_page('https://stackoverflow.com/questions/125703/how-to-modify-a-text-file', soupify=True)
	paras="\n".join(	list(map((lambda x:x.text),page.find_all('p'))) )
	print(paras)
