from common import *
import re
from urlgrab import Cache
from urllib.parse import urljoin
import sys

cache = Cache(debug=False)
url = sys.argv[1]

titlePattern = re.compile("<meta name=\"twitter:title\" content=\"(.+)\">")
authorPattern = re.compile("Created on <strong>[^<]+</strong>\nby <a href=\"https://chyoa.com/user/.+\">(.+)</a>", re.MULTILINE)
contentPattern = re.compile("<div class=\"chapter-content\">(.+)</div>\s+<div class=\"chapter-options\">", re.DOTALL | re.MULTILINE)
questionHeaderPattern = re.compile("<header class=\"question-header\">\n<h2>(.+)</h2>", re.DOTALL | re.MULTILINE)
questionPattern = re.compile("<li><a href=\"(https://chyoa.com/chapter/.+.\d+)\" class=\"\">(.+)</a></li>")

todo = [url]
gotten = set()

mainTitle = None
author = None
newitems = False

while len(todo) > 0:
    current = todo.pop()
    if current in gotten:
        continue
    print(current)
    gotten.add(current)
    data = cache.get(current, max_age = -1).read()

    title = titlePattern.search(data).groups()[0]
    if mainTitle == None:
        mainTitle = title
        author = authorPattern.search(data).groups()[0]
        folder = join("books", mainTitle)
        toc = tocStart(folder)
    
    content = contentPattern.search(data).groups()[0]
    questionHeader = questionHeaderPattern.search(data).groups()[0]
    questions = questionPattern.findall(data)

    print(title, questionHeader, questions)
    content += f"<br />{questionHeader}<br /><ul>\n"
    for questionURL, question in questions:
        content += f"<li><a href=\"{hexdigest_md5(questionURL)}.html\">{question}</a></li>\n"
        todo.append(questionURL)
    content += "</ul>\n"

    newitems = generatePage(current, title, content, folder, toc) or newitems
tocEnd(toc)
makeMobi(folder, author, newitems)