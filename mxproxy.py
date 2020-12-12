import sys;success=0;
importlevel="../";
for i in range(4): 
	if not success:
		try: 
			sys.path.append(importlevel);
			import modulex.modulex as mx ;
			success=1;
		except Exception as e: 
			importlevel=importlevel + "../";
			print(e)
			
if __name__ == '__main__':
	if mx:
		print('modulex success')
	pass