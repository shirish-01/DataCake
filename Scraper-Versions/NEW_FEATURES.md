#	Version 2.0

#	Version 1.3
### + Added More Logging Options
 - now we can showUrlPerSecond=1 and showVisitCount=1 in Logging Module prints stats while running code, to determine the speed of scraper and identify bottlenecks, eventually leading to version 2.0, super fast version with multiprocessing.

### + cleanup Explorer.visit()
 - scraper_utils file is added beside the code to enhance the main code and make it appear less. scraper_utils file has functions fine tuned and intelligently gather data from wodpress blogs, it finds author, body containing highest no of (p tags) and adds timestamp to the json files it creates for each webpage in the profile folder. 
 - extract_info and soup_select under Explorer.visit have been superseded by scraper_utils module -> imported as 'su'
 - reduce failed requests and processing overhead by adding , 404 error handling ie [if page == 404: return]
 - find links on page, now filter out https://www.example.com/image.{jpg,png...} images to reduce overhead.

### + auto default regex 
 - when Explorer is initialized regex default match will be https://website.com/.* but can be mnually set likethis
 - explorer=Explorer(urlinit, myregex=r'/.\*') <-put your regex in myregex.


#	Version 1.1
### +  Added Regex Filtering Module, 
 - change The Regex Condition In Explorer Class > Self.regex . We Can Put Rules Like
 - for Example 
 - url Given As '**https://www.entrepreneur.com/article/35949**'
 - baseurl Becomes Https://www.entrepreneur.com/
 - self.regex= Self.baseurl+r'/article.*' 
 - self.regex 	now Equal To 'https://www.entrepreneur.com/.*'

### +  Added Sanitize Text Option 
 - To Remove Junk Characters Like \n \t Etc, It Can
 - be Customized In Sanitize_text Function, Re.sub Is Used.
 - Explorer.get_all_links() The Regex Condition Is Applied Here, Modifythe Function If
 - Your Requirements To Filter Links Are Different.

### +  Enhanced The Initialization Of Explorer Class, 
 - Now It Automatically Makes A Profile 
 - And Calculate Explored And Visited Links When New Url Is Inputted And Does Not 
 - require To Kickstart It Twice To Get Going.

### +  Removed Repeated Homogenizing Of Files 
 - function At Regular Intervals Ie Remove Duplicate
 - url Entries, Now The Update{explored,visited}urlmemory Functions Only Differentially
 - add New Links And Save Harddisk I/o

### +  Organized Update_exploredurlmemory, Update_visitedurlmemory, Update_pendingurlmemory 
 - to Make Process Atomic And Gain More Precision And Easier Debugging. Nesting Them In
 - previous Versions Were Very Buggy And Tracing Errors Was Very Difficult.

### +  Relative Urls Suport, 
 - /blog => Example.com/blog 

# Version 1.0
## first version with basic functionality.