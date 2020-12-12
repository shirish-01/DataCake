from mxproxy import mx
import re,os,time
import multiprocessing as mp
Cache=mx.Cache

#PATHS-------------------------------------
basedict_path='./Dictionary/dictionary.json' ; mx.touch(basedict_path)
lexico_index_path='./Dictionary/lexico_index.set';	mx.touch(lexico_index_path)
lexico_dict_path='./Dictionary/lexico_dict.jsonl'; 	mx.touch(lexico_dict_path)

#NLP---------------------------------------
def get_lemma(WORD):
	from spacy import load as spacy_load 
	try:
		Cache.nlpengine
	except:
		Cache.nlpengine = spacy_load('en_core_web_sm',disable=['parser','ner', 'tagger', 'textcat'])
	w=Cache.nlpengine(WORD)[0]
	return w.lemma_.lower() if w.lemma_ != '-PRON-' else w.lower_

#CACHE LAYERS------------------------------
Cache.base_dict=mx.jload(basedict_path)
Cache.lexico_index=mx.setload(lexico_index_path)
Cache.lexico_dict=mx.jloadlines(lexico_dict_path)

#CORE--------------------------------------
def get_definition(WORD):
	base_dict=Cache.base_dict
	defn=base_dict.get(WORD) if base_dict.get(WORD) else '' 
	finds=re.findall(r'[\d].*?;',defn)
	if finds:
		return finds
	else:
		return [defn]
#--------------------------------------
def lexico_fetch(WORD): #lower Level
	WORD=get_lemma(WORD)
	while True:
		pagereq=mx.get_page('https://www.lexico.com/definition/'+WORD)
		if pagereq:
			page=mx.soup(pagereq.text,'html.parser')
			break
		if not pagereq:
			print(f'failed :{WORD} Response:{pagereq.text}')
			time.sleep(30)

	finalresult={WORD:[]}
	sections=page.select('.gramb')
	try:
		for section in sections:
			definitions=[x.text.lower() for x in section.select('.semb p .ind')]
			examples=[re.sub(r'[^\w\s]','',x.text) for x in section.select('.trg > div.exg em ')]
			pos=section.select_one('span.pos')
			pos=pos.text if pos else '-'
			pos_def=[{'pos':pos,'def':d,'example':e,} for d,e in zip(definitions,examples)]
			finalresult[WORD].extend(pos_def)
	except Exception as e: 
		open('./Dictionary/ad.log','a').write(str(e)) 
		raise e

	return finalresult

#--------------------------------------

def get_lexico_def(WORD): #Higher Level
	WORD=get_lemma(WORD)
	if WORD in Cache.lexico_index:
		return {WORD:Cache.lexico_dict[WORD]}
	else:
		print(f'added : {WORD}'); # finalresult=POOL.apply(lexico_fetch,(WORD,))
		finalresult=lexico_fetch(WORD)
		update_lexico_db_and_index(WORD,finalresult)
		return finalresult

#--------------------------------------

def update_lexico_db_and_index(WORD,finalresult): #medium level
	mx.fappend(lexico_index_path, WORD)
	if WORD not in Cache.lexico_index:
		print(f'adding ({WORD}) to lexico_index')
		mx.fappend(lexico_dict_path,mx.json.dumps(finalresult))#dump the new word

def build_index_from_dict(dictx,indexPath):#LOGICAL FUNCTION
	keys=[k for k in dictx]
	mx.fwrite(indexPath,'\n'.join(keys))
	# build_index_from_dict(Cache.lexico_dict,lexico_index_path)

def homogenize_dict(dictpath): #LOGICAL FUNCTION
	homdict=[mx.jdumplines({k:v}) for k,v in mx.jloadlines(dictpath).items()]
	homdict='\n'.join(homdict)
	mx.fwrite(dictpath,homdict)
	# homogenize_dict(lexico_dict_path)

def add_words_to_dictionary(words):
	for w in words: get_lexico_def(w)

def seed_dict_with_words():
	#do seeding of dict with standard most common words.
	words={POOL.apply_async(get_lemma, (x.lower(),)) for x in mx.setload('./Dictionary/3000common.set')} ;
	words={x.get() for x in words}
	add_words_to_dictionary(words)

if __name__ == '__main__':
	POOL=mp.Pool(2)

