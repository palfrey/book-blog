Book Blog
=========

Setup
-----
Run `make` to create the protocol buffers files

Usage
-----
python books.py \[options\] (&lt;series name list&gt;)*

Options:

		-h, --help					show this help message and exit
		-c COUNT, --count=COUNT  	Number of items per book (default: 20)

The list of series are in series.txt, and primarily consist of a series of
Regex's defining the title, content and next page link written in [Protocol
Buffers text format][pb]

Generator
---------
Run "python fanfiction.py \<a story URL from FanFiction.net>" to generate a new 
series entry for an arbitrary FanFiction.net story, which can them be copied
into series.txt

Run "python ao3.py \<a story URL from archiveofourown.org>" to generate a new 
series entry for an arbitrary Archive of Our Own story, which can them be copied
into series.txt

[pb]: https://developers.google.com/protocol-buffers/docs/overview
