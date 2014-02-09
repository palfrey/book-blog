from common import *
from urlgrab import Cache
from re import compile, DOTALL, MULTILINE, sub
from urlparse import urljoin

cache = Cache()

titlePattern = compile("<TITLE>(.*?)</TITLE>")
contentPattern = compile("(?:<BR>\s+<BLOCKQUOTE>|<H3 ALIGN=\"CENTER\">)(.+)</BLOCKQUOTE>.+?<A HREF=\"ancilpag.html#DP\">Dramatis personae</A>", DOTALL|MULTILINE) # <A HREF=\"[^\"]+\"><IMG SRC=\"graphics/j-gate.jpg\" ALIGN=\"BOTTOM\" BORDER=\"0\" ALT=\"Into jump gate\"></A>" , DOTALL|MULTILINE)
nextPattern = compile("<A HREF=\"([^\"]+)\"><IMG SRC=\"graphics/j-gate.jpg\" ALIGN=\"BOTTOM\" BORDER=\"0\" ALT=\"Into jump gate\"></A>")

volumePattern = compile("<A HREF=\"(v\dcont.html)\"><IMG HEIGHT=\"\d+\" WIDTH=\"\d+\" SRC=\"graphics/[^\"]+\" ALIGN=\"[^\"]+\" BORDER=\"0\" ALT=\"(Volume \d - [^\"]+)\">")

baseURL = "http://www.b5-dark-mirror.co.uk/"
page = cache.get(baseURL, max_age = -1)
data = page.read()
volumes = sorted(volumePattern.findall(data))

for volumeUrl, volumeTitle in volumes:
	print volumeTitle
	title = "A Dark, Distorted Mirror: " + volumeTitle
	toc = tocStart(title)
	volumePage = cache.get(urljoin(baseURL, volumeUrl), max_age = -1).read()
	splitPattern = compile("<HR><A NAME=\"P[A-Z\d]\"></A>")
	chapterPattern = compile("<A HREF=\"(v\dp.+?.html)\">Chapter (\d+)</A>")
	partPattern = compile(" SIZE=\"\+1\">(.*?)</FONT>")
	for section in splitPattern.split(volumePage):
		chapters = chapterPattern.findall(section)
		if chapters == []:
			continue
		part = sub('<[^>]*>', '', partPattern.findall(section)[0])
		print "\t", part, chapters
		for chapterUrl, _ in chapters:
			url = urljoin(baseURL, chapterUrl)
			print url
			chapterPage = cache.get(url, max_age = -1).read()
			content = contentPattern.search(chapterPage).groups()[0]
			chapterTitle = titlePattern.search(chapterPage).groups()[0]
			generatePage(url, chapterTitle, content, title, toc)
	tocEnd(toc)
	makeMobi(title, "Gareth Williams")
	#break