from codecs import open
from os import mkdir
from os.path import join, exists

try:
	import hashlib
except ImportError: # python < 2.5
	import md5
	hashlib = None

def hexdigest_md5(data):
	if hashlib:
		return hashlib.md5(data).hexdigest()
	else:
		return md5.new(data).hexdigest()

def generatePage(page, title, content, folder, toc):
	fname = hexdigest_md5(page) + ".html"
	fpath = join(folder, fname)
	toc.write("\t\t\t<a title=\"%s\" href=\"%s\" />\n" % (title, fname))
	if not exists(fpath):
		open(fpath, "wb", "utf-8").write(u"""<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
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
	</html>""" % (title, title, content))
		return True
	else:
		return False


def tocStart(folder):
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
	return toc


def tocEnd(toc):
	toc.write("""\t\t</div>
	</body>
</html>""")
	toc.close()