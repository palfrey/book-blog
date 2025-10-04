from common import *
import re
from urlgrab import Cache
from urllib.parse import urljoin

cache = Cache()
cache.user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.3) Gecko/20070309 Firefox/2.0.0.3"

root_url = "http://www.scp-wiki.net/antimemetics-division-hub"
folder = join("books", "SCP - Antimemetics")
toc = tocStart(folder)
content_pattern = re.compile(
    '<div id="page-content">(.+)</div>', re.MULTILINE | re.DOTALL
)
link_pattern = re.compile('<a href="([^"]+)">([^<]+)</a>')

page = cache.get(root_url)
data = content_pattern.search(page.data)
content = data.groups()[0]
links = link_pattern.findall(content)

for link, title in links:
    if (
        link.startswith("http")
        or link.startswith("/scp-")
        or link.startswith("/system:")
        or link.endswith("author-page")
    ):
        continue
    full_link = urljoin(root_url, link)
    print(full_link, title)
    page = cache.get(full_link, max_age=-1).read()
    content = content_pattern.search(page).groups()[0]
    generatePage(full_link, title, content, folder, toc)
tocEnd(toc)
makeMobi(folder, "SCP authors")
