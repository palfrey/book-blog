from sys import argv
from urlgrab import Cache
from codecs import open
import re
from common import *
from urlparse import urljoin

cache = Cache()
url = argv[1]

id = re.search("/works/(\d+)", url)
id = id.groups()[0]

navigate = "http://archiveofourown.org/works/%s/navigate"%id
print navigate

data = cache.get(navigate).read()
data = data.decode("utf-8")
info = re.search("<h2 class=\"heading\">Chapter Index for <a href=\"/works/\d+\">([^<]+)</a> by <a.+href=\"[^\"]+\"[^>]*>([^<]+)</a></h2>", data)
(title, author) = info.groups()

titlePattern = re.compile("<h2 class=\"title heading\">\s+(.*?)\s+</h2>")
summary = re.compile("<div[^>]+?class=\"summary module\"[^>]*?>(.+?)</div>", re.DOTALL|re.MULTILINE)
notes = re.compile("<div.+?class=\"notes module\"[^>]*>(.+?)</div>", re.DOTALL|re.MULTILINE)
mainContent = re.compile("<h3 class=\"landmark heading\" id=\"work\">Chapter Text</h3>(.*?)<!--/main-->", re.DOTALL|re.MULTILINE)
volumePattern = re.compile("<li><a href=\"(/works/\d+/chapters/\d+)\">(\d+). ([^<]+)</a>")

volumes = sorted(volumePattern.findall(data))

print volumes
volumes = dict([(int(x[1]), (x[0],x[2])) for x in volumes])
print volumes

folder = join("books", title)
toc = tocStart(folder)

for volumeUrl, volumeTitle in volumes.values():
	print volumeUrl, volumeTitle
	chapterPage = cache.get(urljoin(navigate, volumeUrl) + "?view_adult=true", max_age = -1).read()
	chapterPage = chapterPage.decode("utf-8")
	items = [summary, notes, mainContent]
	items = [x.search(chapterPage) for x in items]
	items = [x.groups()[0] for x in items if x != None]
	content = "\n".join(items)
	generatePage(volumeUrl, volumeTitle, content, folder, toc)
tocEnd(toc)
makeMobi(folder, author)