from sys import argv
from urlgrab import Cache
from codecs import open
import re

cache = Cache()
url = argv[1]
data = cache.get(url).read()
open("dump", "wb", "utf-8").write(data)

title = re.search("<title>(.+?) Chapter \d+: .+?(, a .+? fanfic)", data)
title = title.groups()
author = re.search("Author: <a href='/u/\d+/[^']+'>([^<]+)</a>", data)
author = author.groups()[0]
name = re.search("self.location = '/s/\d+/'\+ this\.options\[this.selectedIndex\]\.value \+ '/(.+?)';", data)
name = name.groups()[0]
id = re.search("/s/(\d+)", url)
id = id.groups()[0]

print """series {
	name: "%s"
	description: "%s"
	author: "%s"
	titlePattern: "%s (.+?), a"
	startPage: "http://www.fanfiction.net/s/%s/1/%s"
	contentPattern: "<div class='storytext xcontrast_txt' id='storytext'>(.+?)</div>(.*?)</div><div style='height:5px'>"
	nextPattern: "Value='&nbsp;Next &gt;&nbsp;' onClick=\"self.location='([^']+)"
}"""%(title[0].replace(" ",""), title[0], author, title[0], id, name)

