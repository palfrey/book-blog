from common import *
from re import compile, DOTALL, MULTILINE
from urlgrab import Cache
from urllib.parse import urljoin

linkPattern = compile("<h3><a href=\"(/[^\"]+)\">(.+?)</a></h3>")
earlierPattern = compile("<a href='([^\']+)'>.+?Earlier Stories.+?</a>", DOTALL | MULTILINE)
titlePattern = compile("<h2>(.+?)</h2>")
subtitlePattern = compile("<p class=\"standfirst\">(.+?)</p>")
contentPattern = compile("<strong class=\"trailer\">.+?</p>(.+?)(?:(?:<p>(?:(?:<i>)|(?:<small>)|(?:<font size=\"-2\">)|(?:<br>\n))?BOFH .+? Simon Travaglia)|(?:<ul class=\"noindent\">)|(?:<ul>.+?<li><a href=\"http://www.theregister.co.uk/content/30/index.html\">BOFH: The whole shebang</a></li>)|(?:</form>))", DOTALL| MULTILINE)
adPattern = compile("(<div id=ad-mu1-spot>.+?</div>)", MULTILINE | DOTALL)
episodePattern = compile("<strong class=\"trailer\">Episode \d+")

url = "http://www.theregister.co.uk/data_centre/bofh/"
pages = [url]
cache = Cache()

while True:
	print(url)
	data = cache.get(url).read()
	links = linkPattern.findall(data)

	if links == []:
		break

	pages.insert(0, url)

	earlier = earlierPattern.findall(data)
	url = urljoin(url, earlier[0])

skipTitles = ["Salmon Days is Go!"]

year = None

newItems = False

for mainPage in pages:
	data = cache.get(mainPage).read()
	links = linkPattern.findall(data)
	links.reverse()
	for l in links:
		url = urljoin(mainPage, l[0])
		newyear = url.split("/")[3]
		if newyear != year:
			if year != None:
				if int(newyear) < int(year):
					raise Exception(year, newyear)
				tocEnd(toc)
				makeMobi(folder, "Simon Travaglia", newitems = newItems)
				newItems = False
			folder = "BOFH-%s"%newyear
			toc = tocStart(folder)
			year = newyear

		data = cache.get(url, max_age = -1).read()
		episode = episodePattern.findall(data)
		if len(episode) == 0:
			print("Skipping", url)
			continue
		print(url)
		title = titlePattern.findall(data)[0]
		print(title)
		if title in skipTitles:
			print("skipping", title)
			continue
		subtitle = subtitlePattern.findall(data)[0]
		content = contentPattern.findall(data)[0]
		ad = adPattern.findall(data)[0]
		content = content.replace(ad, "")
		content = content.decode('utf-8')
		title = title.decode("utf-8")
		subtitle = subtitle.decode("utf-8")
		assert len(content)>0

		if generatePage(url, title, subtitle + "<br />\n" + content, folder, toc):
			newItems = True
		#break
	print(links)

tocEnd(toc)
makeMobi(folder, "Simon Travaglia")

