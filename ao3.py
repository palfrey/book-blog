from sys import argv
from urlgrab import Cache
from codecs import open
import re

cache = Cache()
url = argv[1]
data = cache.get(url).read()
#open("dump", "wb", "utf-8").write(data)

title = re.search("<title>(.+?) - .+?</title>", data, re.MULTILINE | re.DOTALL)
title = title.groups()[0].strip()
author = re.search("rel=\"author\">([^<]+)</a>", data)
author = author.groups()[0]
id = re.search("/works/(\d+)", url)
id = id.groups()[0]

print """series {
	name: "%s"
	description: "%s"
	author: "%s"
	titlePattern: "<h2 class=\\"title heading\\">\\s+(.*?)\\s+</h2>"
	startPage: "http://archiveofourown.org/works/%s/"
	contentPattern: "<div[^>]+?class=\\"summary module\\"[^>]*?>(.*?)<!--/main-->"
	nextPattern: "<a href=\\"(/works/\d+/chapters/\d+)\\">Next Chapter &#8594;</a>"
}"""%(title.replace(" ",""), title, author, id)
