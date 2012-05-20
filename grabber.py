from urlgrab import Cache
from blog_pb2 import All
from re import compile, DOTALL, MULTILINE
from os import mkdir
from os.path import exists, join
from hashlib import md5

c = Cache()

series = "Tales of Mu"

db = All()
db.ParseFromString(open("series.list", "rb").read())

for s in db.series:
	if s.name == series:
		print s
		page = s.startPage
		index = 1
		while page!=None:
			folder = "%s #%02d"%(s.name, index)
			if not exists(folder):
				mkdir(folder)
			toc = open(join(folder, "toc.html"), "wb")
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
			for x in range(20):
				print "generating", page
				data = c.get(page, max_age=-1).read()
				open("dump", "wb").write(data)

				title = titlePattern.search(data)
				assert title != None, page
				title = title.groups()[0]

				link = nextPattern.search(data)

				content = contentPattern.search(data)
				assert content != None, page
				content = content.groups()[0]

				fname = md5(page).hexdigest() + ".html"
				open (join(folder, fname), "wb").write("""<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
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
				toc.write("\t\t\t<a title=\"%s\" href=\"%s\" />\n"%(title, fname))
				if link != None:
					link = link.groups()[0]
				page = link
				if page == None:
					break
			toc.write("""\t\t</div>
		</body>
	</html>""")
			toc.close()

			if page != None:
				index +=1
