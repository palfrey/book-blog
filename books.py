# -*- coding: utf-8 -*-
from urlgrab import Cache
from google.protobuf import text_format
from blog_pb2 import All
from re import compile, DOTALL, MULTILINE
from os import mkdir, system
from os.path import exists, join
from hashlib import md5
from codecs import open
from sys import argv
from urlparse import urljoin
from optparse import OptionParser

c = Cache()

db = All()
text_format.Merge(open("series.txt","rb","utf-8").read(),db)

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
		if not exists(folder):
			mkdir(folder)
		toc = open(join(folder, "toc.html"), "wb", "utf-8")
		toc.write("""<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<title>%s</title>
	</head>
	<body class="vcenter">
		<div style="display:none">
""" % folder)
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
			fname = md5(page).hexdigest() + ".html"
			fpath = join(folder, fname)

			title = titlePattern.search(data)
			assert title != None, page
			title = title.groups()[0]

			toc.write("\t\t\t<a title=\"%s\" href=\"%s\" />\n"%(title, fname))
			if not exists(fpath):
				newitems = True
				content = contentPattern.search(data)
				assert content != None, page
				content = content.groups()[0]

				open (fpath, "wb", "utf-8").write(u"""<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
		<head>
			<style type="text/css" title="override_css">
				@page {padding: 0pt; margin:0pt}
			</style>
			<title>%s</title>
		</head>
		<body>
			<h1>%s</h1>
			%s
		</body>
	</html>"""%(title, title, content))
			if link != None:
				link = link.groups()[0]
			newpage = urljoin(page, link)
			if page == None or newpage == page:
				page = None
				break
			page = newpage
		toc.write("""\t\t</div>
	</body>
</html>""")
		toc.close()
		if newitems or not exists(folder + ".mobi"):
			cmd = "rm -f book.zip && zip -j book.zip %s/* && ebook-convert book.zip \"%s.mobi\" --output-profile kindle --margin-top 0 --margin-bottom 0 --margin-left 0 --authors=\"%s\" --input-encoding=utf-8" %(folder.replace(" ", "\\ "), folder, s.author)
			print cmd
			system(cmd)

		if page != None:
			index +=1
