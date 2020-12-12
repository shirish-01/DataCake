
# PURPOSE
The Hyperscraper Module Clones The Data On Websites As We Desire. and saves it on harddisk for offline access.
high speed , parallel computing and highly scalable. 

for a given page in website 
- it can collect the webpage body(paragraphs) intelligently using bs4.
- create a timestamp of when it was visited
- collect only images or any specified tag

# Namescheme
- hyperScraper_profiles : is the working directory where all operations takeplace. every url is a profile of scraper.

- hyperScraper_profiles/www.example.com : is nested under hyperScraper_profiles and similar folders are created 
same as website domain name given.  

- hyperScraper_profiles/www.example.com/visited.url : keeps track of which websites have been visited by scraper

- hyperScraper_profiles/www.example.com/explored.url : keeps track of which websites have been Explored by scraper

- hyperScraper_profiles/www.example.com/data : the json objects of webpage are stored here for great compatibility across
different programs. data can be processed further from here.

# Benchmarks
lxml on 256kb data running 100 loops takes 5.5 seconds.
html.parser takes consistently 7.7 seconds. 
html5lib on same size 100 times take 18.5 seconds

# Working:
##the speed is around 20 pages per second on a standard laptop, it can be increased via startThreads(explorer,20) where 20 can be increased. 

- The ' Explorer ' Class Has Various Functions. When Initialized With A Url It Creates A Folder Called hyperscraper_profiles.

- Once Initialized It Will Create The Domain Name Like Www.example.com In Profiles Folder (hyperscraper_profiles). This Is Governed By The Profile_check_make function of Explorer class.

## main logic
- The Principle Variables Are Exploredurlmemory, Visitedurlmemory, Pendingurlmemory. They Are Accesed Within Instance of explorer class , Ie They Are Private Variables... 

- Set Is Very Effecient Data Structure And Has Tremendous Speed. 

- Once Hyperscraper Visits A Page It Discovers New Links And Makes Set{} just visited url is added to Visitedurlmemory{} 

- The Newly discovered Links on the just visited page Are Stored In Exploredurlmemory{} usually 5-30 links are found.

- since we dont want to visit previously visited links, we calculate the difference ie pending links. as shown below. its a list[] since using set{} is causing hash collision when we try to pop a random element for visiting next url.

> 	Pendingurlmemory[] = Explored - visited .

- any file operations have been optimized to make append only to completely remove I/O speed limitation. its achieved via set A-B operation and only the differential is added to file. actually the limitation is CPU since optimizing data takes some computing.

And The Set Operation A-B

- Webvoyage Function Starts Threads And Syncs Multiple Objects Of The explorer Instances, So That Non Linear Scraping Can Takeplace, Failures Are Handled Via Try Except Block to avoid breaking of program.  