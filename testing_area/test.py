# import spacy
# nlp = spacy.load("en_core_web_sm")
# doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
# for ent in doc.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)


#+++++++++++++++++++++++++++++++++++++++++++++++>>> REGEX
# import re
# text='hewlett-packard-$3000,"enterprise partners with wipro to deliver hybrid cloud with hpe greenlake'
# matched=re.sub(r'[\W]',' ',text).split()
# print("-".join(matched))


#+++++++++++++++++++++++++++++++++++++++++++++++>>> BS4 UNIT TESTS
data={
    "url": "https://www.entrepreneur.com/article/348712",
    "head": "COVID-19 Outbreak: Why HRTech Is The Best Tool During These Times",
    "body": "<article id=\"art-v2\"> <div class=\"container\" id=\"art-v2-container\">  <section class=\"art2-holder\" data-word-count=\"445\">   <div class=\"valign-wrapper\">    <a aria-label=\"Coronavirus\" class=\"articlekicker ga-click kickertags\" data-activates=\"tags\" data-ga-action=\"Coronavirus\" data-ga-category=\"article-breadcrumb\" data-ga-label=\"tier.2\" href=\"/topic/coronavirus\" itemprop=\"articleSection\">     Coronavirus    </a>   </div>   <h1 class=\"headline\" itemprop=\"headline\">    COVID-19 Outbreak: Why HRTech Is The Best Tool During These Times   </h1>   <div class=\"art-deck\" itemprop=\"description\">    In a crisis like this, we may be missing out on opportunities to not only increase the efficiency and accuracy of your HR function but also enhance employee engagement   </div>   <div class=\"art-share\">    <div class=\"socialsharebar\" data-author-handle=\"@prasad_rajappan\" data-ga-action=\"display\" data-ga-category=\"article-share-share\" data-ga-label=\"share-348712\" data-share-deck=\"In a crisis like this, we may be missing out on opportunities to not only increase the efficiency and accuracy of your HR function but also...\" data-share-title=\"COVID-19 Outbreak: Why HRTech Is The Best Tool During These Times\" data-share-url=\"http://entm.ag/5vc1\" data-shareid=\"share348712article-share\" id=\"share348712article-share\">     <a class=\"btn-flat ga-click right uppercase bold\" data-ga-action=\"click\" data-ga-category=\"article-next-button-355635\" data-ga-label=\"Next Article Button\" data-next=\"/article/355635\" href=\"/article/355635\">      Next Article      <i class=\"icon-arrow-right right\">      </i>     </a>     <ul>      <li class=\"count\">       <span id=\"ent-share-count-display\">        --       </span>       shares      </li>      <li class=\"ga-click socialcolor facebook solid\" data-ga-action=\"facebook\" data-ga-category=\"article-share-share\" data-ga-label=\"share-348712\" data-network=\"facebook\" title=\"Share on Facebook\">       <i class=\"icon-facebook\">       </i>      </li>      <li class=\"ga-click socialcolor twitter solid\" data-ga-action=\"twitter\" data-ga-category=\"article-share-share\" data-ga-label=\"share-348712\" data-network=\"twitter\" title=\"Share on Twitter\">       <i class=\"icon-twitter\">       </i>      </li>      <li class=\"ga-click socialcolor linkedin solid\" data-ga-action=\"linkedin\" data-ga-category=\"article-share-share\" data-ga-label=\"share-348712\" data-network=\"linkedin\" title=\"Share on LinkedIn\">       <i class=\"icon-linkedin\">       </i>      </li>      <li class=\"ga-click black solid sharelink\" data-ga-action=\"clipboard\" data-ga-category=\"article-share-share\" data-ga-label=\"share-348712\" data-network=\"sharelink\" title=\"Copy Link\">       <i class=\"material-icons link-icon\">        link       </i>      </li>     </ul>     <a class=\"qs addqueue btn btn-inverse btn-small hide-on-small-only gutter-left ga-click\" data-ga-action=\"click\" data-ga-category=\"article-share-queue\" data-ga-label=\"queue-348712\" data-queueaction=\"add\" data-queueitemid=\"348712\" data-queuetype=\"article\" href=\"#\" title=\"Add to your queue\">      Add to Queue     </a>    </div>   </div>   <div class=\"hero-ad\">    <div class=\"island-ad adbox\" data-adsync=\"true\" data-key=\"vad\">    </div>   </div>   <figure class=\"heroimage\">    <div class=\"imgcont\">     <img alt=\"COVID-19 Outbreak: Why HRTech Is The Best Tool During These Times\" class=\"lazy lazyload\" data-src=\"https://assets.entrepreneur.com/content/3x2/2000/20200403142715-human-resources.jpeg?width=700&amp;crop=2:1\" itemprop=\"image\" itemscope=\"\" itemtype=\"https://schema.org/ImageObject\" src=\"https://assets.entrepreneur.com/content/3x2/2000/20200403142715-human-resources.jpeg?width=700&amp;crop=2:1&amp;blur=50\"/>     <div class=\"credit\">      Image credit:Pixabay     </div>    </div>   </figure>   <div class=\"author-info\">    <a class=\"hero ga-click\" data-ga-action=\"click\" data-ga-category=\"article.author\" data-ga-label=\"image\" href=\"/author/prasad-rajappan\" itemprop=\"author\" itemscope=\"\" itemtype=\"https://schema.org/Person\" rel=\"author\">     <img alt=\"Prasad Rajappan\" src=\"https://assets.entrepreneur.com/content/1x1/300/20180606100005-0.jpeg?width=100\"/>    </a>    <div class=\"block\">     <a class=\"authorname ga-click\" data-ga-action=\"click\" data-ga-category=\"article.author\" data-ga-label=\"name\" href=\"/author/prasad-rajappan\" itemprop=\"author\" itemscope=\"\" itemtype=\"https://schema.org/Person\" rel=\"author\" title=\"Prasad Rajappan: Article Author\">      <div itemprop=\"name\">       Prasad Rajappan      </div>     </a>     <div class=\"prohead\">      CEO, Founder, Zing     </div>     <div class=\"socialaccounts\">      <a aria-label=\"twitter\" class=\"twitter ga-click\" data-ga-action=\"click\" data-ga-category=\"article.author.social\" data-ga-label=\"twitter\" href=\"https://twitter.com/prasad_rajappan\" target=\"_blank\">       <i class=\"icon-twitter\">       </i>      </a>      <a aria-label=\"linkedin\" class=\"linkedin ga-click\" data-ga-action=\"click\" data-ga-category=\"article.author.social\" data-ga-label=\"linkedin\" href=\"https://www.linkedin.com/in/prasad-rajappan-a002a73/\" target=\"_blank\">       <i class=\"icon-linkedin\">       </i>      </a>     </div>    </div>   </div>   <div class=\"art-v2-body\" id=\"articleAdd\">    <div class=\"gate-check\">     <div class=\"fs-h grey-text text-darken-1 ff-default\">      <time content=\"2020-04-03T14:27:00Z\" datetime=\"2020-04-03 14:27:00\" itemprop=\"datePublished\">       April3, 2020      </time>      3 min read     </div>     <div class=\"fs-k grey-text text-darken-1 light gutter-top\">      Opinions expressed by      <em>       Entrepreneur      </em>      contributors are their own.     </div>     <small class=\"grey-text text-darken-1\">     </small>     <p>      Even before the contagious coronavirus spread, the pandemic forced the workforce to shift to work from home. But are we taking advantage of top HR tech tools? Especially in a crisis like this, we may be missing out on opportunities to not only increase the efficiency and accuracy of your HR function but also enhance employee engagement.     </p>     <p>      HR tools can help you increase the productivity of the employees and help your business function smoothly.     </p>     <p>      Here are the tools which you can consider:     </p>     <p>      <b>       Make Sure Your Employees Get Recognized      </b>     </p>     <p>      Employee engagement has emerged as a critical driver for success of businesses today. A lot of organizations are recognizing their employees who are going above and beyond to contribute to these challenging times. Induce a sense of belongingness, closeness and friendliness within your organization.     </p>     <p>      <b>       Employees Are Marked For Their Hard Work      </b>     </p>     <p>      Geo-fencing mobile-based punch-in/punch-out will make sure that your attendance is marked for the day you have worked on and gets you digitally connected workforce. Geo-fencing lets you better collaborate and manage work from home for employees while enabling businesses to ensure performance and productivity.     </p>     <p>      <b>       Keep Your Employees In the Loop      </b>     </p>     <p>      Educate your employees on dos and don\u2019ts by announcing updates on your company announcement forums or internal communication channels. Connect seamlessly with everyone irrespective of any location or time and keep them up to date to quell rumors amid COVID-19.     </p>     <p>      <b>       Make Sure Employees Get Paid on Time      </b>     </p>     <p>      During this difficult hour and overall lockdown situations, while all your employees are putting their best in this situation, organizations should think of making life slightly easier for them by processing their salaries on time. Make sure your employees are paid on time with faster processing and assured accuracy.     </p>     <p>      <b>       Upskill Yourself and Make the Most Of the Lockdown Period      </b>     </p>     <p>      Keep training and keep learning until you get it right. Learning can never go waste and you can certainly use tools such as learning management system to study new courses, learn new domains and expand your array. With learning management systems, you can ensure contactless knowledge and information dissemination with mobile-based learning. A lot of organizations can leverage collaborative tools like forum discussions, wikis to improve communication and collaboration within the teams. E-Learning with gamification can truly create a rich, interactive and engaging learning experience.     </p>     <p>      We can see that the numbers are expected to rise with the dangers posed by the virus outbreak. Due to this pandemic, millions of the workforce across the globe are working from home and the HR function along with the businesses at large have found that HRtech is the best bet during these testing times to improve the team collaboration, productivity and keep achieving the business outcomes.     </p>    </div>    <div class=\"entnatv clearfix\" data-type=\"article-footer-promo\">    </div>   </div>  </section> </div></article>",
    "time": "41.0 Days Ago",
    "imgs": "[<img alt=\"COVID-19 Outbreak: Why HRTech Is The Best Tool During These Times\" class=\"lazy lazyload\" data-src=\"https://assets.entrepreneur.com/content/3x2/2000/20200403142715-human-resources.jpeg?width=700&amp;crop=2:1\" itemprop=\"image\" itemscope=\"\" itemtype=\"https://schema.org/ImageObject\" src=\"https://assets.entrepreneur.com/content/3x2/2000/20200403142715-human-resources.jpeg?width=700&amp;crop=2:1&amp;blur=50\"/>, <img alt=\"Prasad Rajappan\" src=\"https://assets.entrepreneur.com/content/1x1/300/20180606100005-0.jpeg?width=100\"/>]"
}

from bs4 import BeautifulSoup as soup
import time

data2=open('dummy.html','r',encoding='utf-8').read()

# data2='<p><img alt="image20" class="aligncenter size-full wp-image-16018 lazyloaded" data-ll-status="loaded" height="770" sizes="(max-width: 1024px) 100vw, 1024px" src="https://neilpatel.com/wp-content/uploads/2016/05/image20-6.png" srcset="https://neilpatel.com/wp-content/uploads/2016/05/image20-6.png 1024w, https://neilpatel.com/wp-content/uploads/2016/05/image20-6-350x263.png 350w, https://neilpatel.com/wp-content/uploads/2016/05/image20-6-768x578.png 768w, https://neilpatel.com/wp-content/uploads/2016/05/image20-6-700x526.png 700w" width="1024"/></p>'
mysoup=soup(data2,'html5lib')

ta=time.time()

targetbody=mysoup.p.parent.extract()

elist=targetbody.find_all('span')

def tag_unwrapper(tagname,input):
	pass

for x in targetbody.findAll():
	try:
		for s in x.findAll('span'):
			s=s.unwrap()
			...
	except Exception as e:
		# print(e)
		# raise e
		...

try:
	c=0
	arr=targetbody.find_all('img')
	for item in arr :
		# newtag=mysoup.new_tag('img',src=arr[c]['src'])
		freez_attrs=list(arr[c].attrs.keys())
		for attr in freez_attrs:
			if attr != 'src':
				del item[attr]
		print(item)

		# arr[c].replace_with(newtag)
		c+=1
except Exception as e:
	print(e)
	raise e
	...

print(targetbody)
# print(dir(targetbody))