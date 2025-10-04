from common import *
from sys import argv
from urlgrab import Cache
from re import compile, DOTALL, MULTILINE

cache = Cache()
url = argv[1]

titlePattern = compile("<h1>([^<]+)</h1>")
contentPattern = compile(
    '<div class="b-story-body-x x-r15">(.+?)</div><div class="b-story-stats-block">',
    DOTALL | MULTILINE,
)
nextPattern = compile('"([^"]+)">Next</a>')

chapterPattern = compile("(.*?) (?:Ch.|Pt.) (\d+)")
memberPattern = compile(
    '<a href="(https://www.literotica.com/stories/memberpage.php\?uid=\d+&amp;page=submissions)">([^<]+)</a>'
)
chapterLinkPattern = compile('href="(https://www.literotica.com/s/[^"]+)">([^<]+)</a>')

page = cache.get(url, max_age=-1)
data = page.read()
open("dump", "wb").write(data.encode("utf-8"))

title = titlePattern.findall(data)
title = title[0]

chapter = chapterPattern.match(title)
if chapter != None:
    title = chapter.groups()[0]
    currentChapter = 1

print(title)
folder = join("books", title)

toc = tocStart(folder)
memberPage = memberPattern.search(data)
memberData = cache.get(
    memberPage.groups()[0].replace("&amp;", "&"), max_age=3600
).read()
author = memberPage.groups()[1]
if chapter != None:
    links = chapterLinkPattern.findall(memberData)
    chapterLinks = {}
    for l in links:
        ch = chapterPattern.search(l[1])
        if ch != None and ch.groups()[0] == title:
            chapterLinks[int(ch.groups()[1])] = l[0]

    open("dump", "wb").write(memberData.encode("utf-8"))
    print("links", chapterLinks)

while True:
    if chapter != None and url != chapterLinks[currentChapter]:
        print("getting", currentChapter)
        page = cache.get(chapterLinks[currentChapter], max_age=-1)
        url = chapterLinks[currentChapter]
        print(url)
        data = page.read()
    chapterTitle = titlePattern.findall(data)
    chapterTitle = chapterTitle[0]
    content = ""
    while True:
        contentMatch = contentPattern.findall(data)
        content += contentMatch[0]
        # print content
        nextMatch = nextPattern.findall(data)
        if nextMatch == []:
            break

        nextURL = nextMatch[0]
        print(nextURL)
        page = cache.get(nextURL, max_age=-1)
        data = page.read()

    generatePage(url, chapterTitle, content, folder, toc)
    if chapter == None:
        break
    currentChapter += 1
    if currentChapter not in chapterLinks:
        break
tocEnd(toc)
makeMobi(folder, author)
