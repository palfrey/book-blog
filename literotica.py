from common import *
from sys import argv
from urlgrab import Cache
from re import compile, DOTALL, MULTILINE

cache = Cache()
url = argv[1]

titlePattern = compile("<h1>([^<]+)</h1>")
contentPattern = compile("<div class=\"b-story-body-x x-r15\">(.+?)</div><div class=\"b-story-stats-block\">" , DOTALL|MULTILINE)
nextPattern = compile("\"([^\"]+)\">Next</a>")

page = cache.get(url, max_age = -1)
data = page.read()
open("dump", "wb").write(data)

title = titlePattern.findall(data)
print title
title = title[0]
content = u""
while True:
	contentMatch = contentPattern.findall(data)
	print page.headers.headers
	print type(data)
	content += contentMatch[0]
	#print content
	nextMatch = nextPattern.findall(data)
	if nextMatch == []:
		break

	nextURL = nextMatch[0]
	print nextURL
	page = cache.get(nextURL, max_age=-1)
	data = page.read()


toc = tocStart(title)
generatePage(url, title, content, title, toc)
tocEnd(toc)
