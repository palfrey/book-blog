from os import listdir, system
from os.path import isdir, exists

for x in sorted(listdir(".")):
	if not isdir(x):
		continue
	if x in ("urlgrab", "cache") or x[0] == ".":
		continue
	fname = x + ".mobi"
	if not exists(fname):
		print fname
		cmd = "rm -f tom.zip && zip -j tom.zip %s/* && ebook-convert tom.zip \"%s\" --output-profile kindle --margin-top 0 --margin-bottom 0 --margin-left 0 --authors=\"Alexandra Erin\" --enable-heuristics" %(x.replace(" ", "\\ "), fname)
		print cmd
		system(cmd)

