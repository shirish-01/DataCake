def file_namer(text): 
	return "-".join(	re.sub(r'[\W]',' ',text).split())

def time_stamper(maxdaysago):
	pass

def soup_select(soup,bs_select):
	try: return sanitize_text(soup.select_one(bs_select).prettify()) 
	except: return 'UNKNOWN'

def sanitize_text(text): 
	return re.sub(	r'\n|\t','',text)