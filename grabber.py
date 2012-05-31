# -*- coding: utf-8 -*-
from urlgrab import Cache
from blog_pb2 import All
from re import compile, DOTALL, MULTILINE
from os import mkdir, system
from os.path import exists, join
from hashlib import md5
from codecs import open
from sys import argv
from urlparse import urljoin

c = Cache()

db = All()
db.ParseFromString(open("series.list", "rb").read())

wrong = {
		u"â€œ": u"\"",
		u"â€™": u"'",
		u"â€": u"\"",
		u"â€˜": u"'",
		u"â€”": u" - ",
		u"â€¦": u"-",
		}

for s in db.series:
	if s.name in argv[1:]:
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
			for x in range(20):
				print "generating", page
				p = c.get(page, max_age=-1)
				data = p.read().decode("utf-8")

				for k in wrong:
					data = data.replace(k, wrong[k])

				open("dump", "wb", "utf-8").write(data)

				link = nextPattern.search(data)
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
				page = link
				if page == None:
					break
			toc.write("""\t\t</div>
		</body>
	</html>""")
			toc.close()
			if newitems or not exists(folder + ".mobi"):
				cmd = "rm -f book.zip && zip -j book.zip %s/* && ebook-convert book.zip \"%s.mobi\" --output-profile kindle --margin-top 0 --margin-bottom 0 --margin-left 0 --authors=\"%s\"" %(folder.replace(" ", "\\ "), folder, s.author)
				print cmd
				system(cmd)

			if page != None:
				index +=1
