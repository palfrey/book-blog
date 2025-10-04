from codecs import open
from os import mkdir, system
from os.path import join, exists, getsize
import platform

import hashlib


def hexdigest_md5(data):
    return hashlib.md5(data.encode("utf-8")).hexdigest()


def generatePage(page, title, content, folder, toc):
    fname = str(hexdigest_md5(page) + ".html")
    fpath = join(folder, fname)
    toc.write('\t\t\t<a class="toc_title" href="%s">%s</a>\n' % (fname, title))
    if not exists(fpath) or getsize(fpath) < 500:
        open(fpath, "wb", "utf-8").write(
            """<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
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
	</html>"""
            % (title, title, content)
        )
        return True
    else:
        return False


def tocStart(folder):
    if not exists(folder):
        mkdir(folder)
    toc = open(join(folder, "toc.html"), "wb", "utf-8")
    toc.write(
        """<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<title>%s</title>
	</head>
	<body class="vcenter">
		<div style="display:none">
"""
        % folder.split("/")[-1]
    )
    return toc


def tocEnd(toc):
    toc.write(
        """\t\t</div>
	</body>
</html>"""
    )
    toc.close()


def makeMobi(folder, author, newitems=False):
    if newitems or not exists(folder + ".mobi"):
        if platform.system() == "Linux":
            cmd = (
                "rm -f book.zip && zip -j book.zip %s/* && ebook-convert book.zip \"%s.mobi\" --output-profile kindle --margin-top 0 --margin-bottom 0 --margin-left 0 --authors=\"%s\" --input-encoding=utf-8 --level1-toc '//*[@class='toc_title']' --no-chapters-in-toc --toc-threshold=1 --max-toc-links=0"
                % (folder.replace(" ", "\\ ").replace("'", "\\'"), folder, author)
            )
        elif platform.system() == "Darwin":
            cmd = (
                "rm -f book.zip && zip -j book.zip %s/* && /Applications/calibre.app/Contents/MacOS/ebook-convert book.zip \"%s.mobi\" --output-profile kindle --margin-top 0 --margin-bottom 0 --margin-left 0 --authors=\"%s\" --input-encoding=utf-8 --level1-toc '//*[@class='toc_title']' --no-chapters-in-toc --toc-threshold=1 --max-toc-links=0"
                % (folder.replace(" ", "\\ ").replace("'", "\\'"), folder, author)
            )
        else:
            raise Exception("Unknown system: %s" % platform.system())
        print(cmd)
        system(cmd)


def makeEpub(folder, author, newitems=False):
    if newitems or not exists(folder + ".epub"):
        cmd = (
            "rm -f book.zip && zip -j book.zip %s/* && ebook-convert book.zip \"%s.epub\" --output-profile kindle --margin-top 0 --margin-bottom 0 --margin-left 0 --authors=\"%s\" --input-encoding=utf-8 --level1-toc '//*[@class='toc_title']' --no-chapters-in-toc --toc-threshold=1 --max-toc-links=0"
            % (folder.replace(" ", "\\ ").replace("'", "\\'"), folder, author)
        )
        print(cmd)
        system(cmd)
