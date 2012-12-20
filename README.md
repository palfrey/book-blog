Book Blog
=========

Setup
-----
Run `make` to create the protocol buffers files

Usage
-----
books.py \[options\] (&lt;series name list&gt;)*

Options:

		-h, --help					show this help message and exit
		-c COUNT, --count=COUNT  	Number of items per book (default: 20)

The list of series are in series.txt, and primarily consist of a series of
Regex's defining the title, content and next page link written in [Protocol
Buffers text format][pb]

[pb]: https://developers.google.com/protocol-buffers/docs/overview
