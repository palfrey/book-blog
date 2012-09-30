# -*- coding: utf-8 -*-
from urlgrab import Cache
from google.protobuf import text_format
from blog_pb2 import All
from re import compile, DOTALL, MULTILINE
from os import  system
from os.path import exists
from codecs import open
from urlparse import urljoin
from optparse import OptionParser
from common import generatePage, tocStart, tocEnd

c = Cache()

db = All()
text_format.Merge(open("series.txt","rb","utf-8").read(),db)

# Kindle doesn't like various characters, so lets rewrite some of them...
wrong = {
		u"â€œ": u"\"",
		u"â€™": u"'",
		u"â€": u"\"",
		u"â€˜": u"'",
		u"â€”": u" - ",
		u"â€¦": u"-",
		u"": u"",
		}

series = dict([(s.name,s) for s in db.series])

parser = OptionParser(usage="%prog [options] (<series name list>)*")
parser.add_option("-c", "--count", dest="count", default=20, help="Number of items per book (default: 20)", type=int)

opts, args = parser.parse_args()

seriesDisplay = "\t" + "\n\t".join(["%s (%s)"%(s.name, s.description) for s in series.values()])

if len(args) == 0:
	parser.error("Need some series. Options are: \n" + seriesDisplay)

for k in args:
	if k not in series.keys():
		parser.error("Can't find series '%s'. Options are: \n"%k + seriesDisplay)

series = [series[k] for k in args]

for s in series:
	print s
	page = s.startPage
	index = 1
	while page!=None:
		folder = "%s #%02d"%(s.description, index)
		toc = tocStart()
		titlePattern = compile(s.titlePattern, DOTALL | MULTILINE)
		contentPattern = compile(s.contentPattern, DOTALL | MULTILINE)
		nextPattern = compile(s.nextPattern, DOTALL | MULTILINE)
		newitems = False
		for x in range(opts.count):
			print "generating", page
			age = -1
			while True:
				p = c.get(page, max_age=age)
				data = p.read().decode("utf-8")

				for k in wrong:
					data = data.replace(k, wrong[k])

				open("dump", "wb", "utf-8").write(data)

				link = nextPattern.search(data)
				if link == None and age == -1:
					age = 3600
				else:
					break
			title = titlePattern.search(data)
			assert title != None, page
			title = title.groups()[0]
			content = contentPattern.search(data)
			assert content != None, page
			content = content.groups()[0]
			newitems = generatePage(title, content, folder, toc) or newitems
			if link is not None:
				link = link.groups()[0]
			newpage = urljoin(page, link)
			if page == None or newpage == page:
				page = None
				break
			page = newpage
		tocEnd(toc)
		if newitems or not exists(folder + ".mobi"):
			cmd = "rm -f book.zip && zip -j book.zip %s/* && ebook-convert book.zip \"%s.mobi\" --output-profile kindle --margin-top 0 --margin-bottom 0 --margin-left 0 --authors=\"%s\" --input-encoding=utf-8" %(folder.replace(" ", "\\ "), folder, s.author)
			print cmd
			system(cmd)

		if page != None:
			index +=1
