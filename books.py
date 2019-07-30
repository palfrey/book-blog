# -*- coding: utf-8 -*-
from urlgrab import Cache
from google.protobuf import text_format
from blog_pb2 import All
from re import compile, DOTALL, MULTILINE
from os.path import exists, join
from codecs import open
from urllib.parse import urljoin
from optparse import OptionParser
from common import generatePage, tocStart, tocEnd, makeMobi

c = Cache()
c.user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.3) Gecko/20070309 Firefox/2.0.0.3"

db = All()
text_format.Merge(open("series.txt","rb","utf-8").read(),db)
stripTags = compile("<[^>]+>");
stripAnchorTags = compile("(?:<a[^>]+>)|(?:</a>)");

# Kindle doesn't like various characters, so lets rewrite some of them...
wrong = {
		"â€œ": "\"",
		"â€™": "'",
		"â€": "\"",
		"â€˜": "'",
		"â€”": " - ",
		"â€¦": "-",
		"": "",
		'“': "\"",
		'”':"\"",
		'–':"-",
		'’':"'",
		' ':" ",
		'ñ':"&ntilde;",
		'…':'&hellip;',
		'‘':'\'',
		}

series = dict([(s.name,s) for s in db.series])

parser = OptionParser(usage="%prog [options] (<series name list>)*")
parser.add_option("-c", "--count", dest="count", default=20, help="Number of items per book (default: 20)", type=int)

opts, args = parser.parse_args()

seriesDisplay = "\t" + "\n\t".join(["%s (%s)"%(s.name, s.description) for s in list(series.values())])

if len(args) == 0:
	parser.error("Need some series. Options are: \n" + seriesDisplay)

for k in args:
	if k not in list(series.keys()):
		parser.error("Can't find series '%s'. Options are: \n"%k + seriesDisplay)

series = [series[k] for k in args]

def infiniteRange():
	i = 1
	while True:
		yield i
		i +=1

for s in series:
	print(s)
	if s.description == "":
		s.description = s.name
	page = s.startPage
	index = 1
	while page!=None:
		if opts.count == -1:
			folder = s.description
		else:
			folder = "%s #%02d"%(s.description, index)
		folder = join("books", folder)
		toc = tocStart(folder)
		titlePattern = compile(s.titlePattern, DOTALL | MULTILINE)
		contentPattern = compile(s.contentPattern, DOTALL | MULTILINE)
		nextPattern = compile(s.nextPattern, DOTALL | MULTILINE)
		newitems = False
		if opts.count == -1:
			items = infiniteRange()
		else:
			items = list(range(opts.count))

		for x in items:
			print(("generating", page))
			age = -1
			while True:
				p = c.get(page, max_age=age)
				data = p.read()

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
			title = title.groups()[0].replace("\n", "")
			title = stripTags.sub("", title)
			content = contentPattern.search(data)
			assert content != None, page
			content = content.groups()[0]
			content = content.strip()
			content = stripAnchorTags.sub("", content)
			assert len(content) > 30, (folder, page, content)
			newitems = generatePage(page, title, content, folder, toc) or newitems
			if link is not None:
				link = link.groups()[0]
			newpage = urljoin(page, link)
			if page == None or newpage == page:
				page = None
				break
			page = newpage + "?view_adult=true"
		tocEnd(toc)
		makeMobi(folder, s.author, newitems)

		if page != None:
			index +=1
