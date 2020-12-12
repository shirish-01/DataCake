from mxproxy import mx
Cache=mx.Cache

#INITIALIZATION_______________________
lexico_syn_path='./Dictionary/lexico_syn.jsonl'; 	mx.touch(lexico_syn_path)
lexico_syn_index_path='./Dictionary/lexico_syn_index.set'; mx.touch(lexico_syn_index_path)

Cache.lexico_syn_index=mx.setload(lexico_syn_index_path)
Cache.lexico_syn=mx.jloadlines(lexico_syn_path)

#-------------------------------------
def get_lemma(WORD):
	from spacy import load as spacy_load 
	try:
		Cache.nlpengine
	except:
		Cache.nlpengine = spacy_load('en_core_web_sm',disable=['parser','ner', 'tagger', 'textcat'])
	w=Cache.nlpengine(WORD)[0]
	return w.lemma_.lower() if w.lemma_ != '-PRON-' else w.lower_

def db_sync(WORD,finalresult):
	if WORD not in Cache.lexico_syn_index:
		mx.fappend(lexico_syn_index_path, WORD)
		print(f'adding \'{WORD}\' to Thesaurus')
		mx.fappend( lexico_syn_path, mx.json.dumps(finalresult) )#dump the new word
	Cache.lexico_syn_index.add(WORD)

def get_lexico_syn(WORD): #medium level 
	if WORD in Cache.lexico_syn:
		print(f'syn: {WORD} found in db')
		return {WORD:Cache.lexico_syn[WORD]}
	else:
		WORD=get_lemma(WORD.lower())
		synGroups=mx.get_page_soup(f'https://www.lexico.com/synonyms/{WORD}').select('.synGroup')
		removeWaste=[[y.decompose() for y in x.findAll(class_=lambda z: 'syn' not in z)] for x in synGroups ]
		sortedWords=[[y.strip() for y in x.text.split(',')] for x in synGroups]
		theresult={WORD:sortedWords}
		db_sync(WORD,theresult)
		return theresult

if __name__ == '__main__':
	res=get_lexico_syn('shoot')
	print(dir(Cache),res)