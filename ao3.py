from sys import argv
from urlgrab import Cache
from codecs import open, decode
import re
from common import *
from urllib.parse import urljoin

cache = Cache()
url = argv[1]

id = re.search("/works/(\d+)", url)
id = id.groups()[0]

navigate = "https://archiveofourown.org/works/%s/navigate"%id
print(navigate)

data = cache.get(navigate).read()
info = re.search("<h2 class=\"heading\">Chapter Index for <a href=\"/works/\d+\">([^<]+)</a> by <a.+href=\"[^\"]+\"[^>]*>([^<]+)</a></h2>", data)
(title, author) = info.groups()

titlePattern = re.compile("<h2 class=\"title heading\">\s+(.*?)\s+</h2>")
summary = re.compile("<div[^>]+?class=\"summary module\"[^>]*?>(.+?)</div>", re.DOTALL|re.MULTILINE)
notes = re.compile("<div.+?class=\"notes module\"[^>]*>(.+?)</div>", re.DOTALL|re.MULTILINE)
mainContent = re.compile("<h3 class=\"landmark heading\" id=\"work\">Chapter Text</h3>(.*?)<!--/main-->", re.DOTALL|re.MULTILINE)
volumePattern = re.compile("<li><a href=\"(/works/\d+/chapters/\d+)\">(\d+). ([^<]+)</a>")

volumes = sorted(volumePattern.findall(data))

print(volumes)
volumes = dict([(int(x[1]), (x[0],x[2])) for x in volumes])
print(volumes)

folder = join("books", title)
toc = tocStart(folder)

newitems = False
for volumeUrl, volumeTitle in list(volumes.values()):
	print(volumeUrl, volumeTitle)
	chapterPage = cache.get(urljoin(navigate, volumeUrl) + "?view_adult=true", max_age = -1).read()
	if type(chapterPage) != str:
		chapterPage = str(chapterPage, "utf-8", "replace")
	items = [summary, notes, mainContent]
	items = [x.search(chapterPage) for x in items]
	items = [x.groups()[0] for x in items if x != None]
	content = "\n".join(items)
	newitems = generatePage(volumeUrl, volumeTitle, content, folder, toc) or newitems
tocEnd(toc)
makeMobi(folder, author, newitems)