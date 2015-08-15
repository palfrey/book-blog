from sys import argv
from urlgrab import Cache
from codecs import open
import re

cache = Cache()
url = argv[1]
data = cache.get(url).read()
open("dump", "wb", "utf-8").write(data)

title = re.search("<title>(.+?) Chapter \d+", data)
title = title.groups()
author = re.search("By:</span> <a[^>]+?href='/u/\d+/[^']+'>([^<]+)</a>", data)
author = author.groups()[0]
id = re.search("/s/(\d+)", url)
id = id.groups()[0]

print """series {
	name: "%s"
	description: "%s"
	author: "%s"
	startPage: "http://m.fanfiction.net/s/%s/1"
	titlePattern: "<img src='//[^']+/balloon.png' class='mt icons'>[\d,]+</a></span>(.+?)<br>"
	contentPattern: "id='storycontent' >(.+?)</div></div>.*?<hr size=1"
	nextPattern: "<a href='(/s/\d+/\d+/)'>Next &#187;</a>"
}"""%(title[0].replace(" ",""), title[0], author, id)

