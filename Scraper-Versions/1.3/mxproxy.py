import sys;success=0;importlevel="../";
try:#try in ./
	import modulex as mx
except Exception as e:
	...

for i in range(4): #try in ../../.....
	if not success:
		try: sys.path.append(importlevel);from modulex import modulex as mx ;success=1;mx.cleanup();print("mx imported")
		except Exception as e: importlevel=importlevel + "../";

if __name__ == '__main__':
	page=mx.get_page('https://stackoverflow.com/questions/125703/how-to-modify-a-text-file', soupify=True)
	paras="\n".join(	list(map((lambda x:x.text),page.find_all('p'))) )
	print(paras)
