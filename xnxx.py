from common import *
from sys import argv
from urlgrab import Cache
from re import compile, DOTALL, MULTILINE, UNICODE
from urlparse import urljoin
from text2num import text2num

cache = Cache()
url = argv[1]

titlePattern = compile("<span class=\"titre_story\">\s+(.+?)\s+</span>", MULTILINE | UNICODE)
contentPattern = compile("<td class=\"bandeau_td_2\" [^>]+>(.+?)<span class=\"texte_comment_blanc\">" , DOTALL|MULTILINE)

chapterPattern = compile("(.*?) - Chapter ([^ ]+) - (.+)")
memberPattern = compile("<a class=\"link_page_stories\" href=\"(/profile\d+/[^\"]+)\">([^<]+)</a>")
chapterLinkPattern = compile("class=\"link_stories\" href=\"(/story/\d+/[^\"]+)\">([^<]+)</a>")

page = cache.get(url, max_age = -1)
data = page.read()
open("dump", "wb").write(data.encode("utf-8"))

title = titlePattern.findall(data)
title = title[0]

chapter = chapterPattern.match(title)
if chapter != None:
	title = chapter.groups()[0]
	currentChapter = 1

print "\"%s\"" % title

toc = tocStart(title)
memberPage = memberPattern.search(data)
memberData = cache.get(urljoin(url, memberPage.groups()[0].replace("&amp;", "&")), max_age=3600).read()
author = memberPage.groups()[1]

if chapter != None:
	links = chapterLinkPattern.findall(memberData)
	chapterLinks = {}
	for l in links:
		ch = chapterPattern.search(l[1])
		if ch != None and ch.groups()[0] == title:
			try:
				chapterLinks[int(ch.groups()[1])] = l[0]
			except ValueError:
				val = text2num(ch.groups()[1].lower())
				chapterLinks[val] = l[0]

	open("dump", "wb").write(memberData.encode("utf-8"))
	print "links", chapterLinks

while True:
	if chapter !=None and url != chapterLinks[currentChapter]:
		print "getting", currentChapter
		url = urljoin(url, chapterLinks[currentChapter])
		page = cache.get(url, max_age = -1)
		print url
		data = page.read()
	chapterTitle = titlePattern.findall(data)
	chapterTitle = chapterPattern.search(chapterTitle[0])
	chapterTitle = "Chapter %s - %s"%(currentChapter, chapterTitle.groups()[2])
	contentMatch = contentPattern.findall(data)
	content = contentMatch[0]

	generatePage(url, chapterTitle, content, title, toc)
	if chapter == None:
		break
	currentChapter +=1
	if currentChapter not in chapterLinks:
		break
tocEnd(toc)
makeMobi(title, author, True)
	
