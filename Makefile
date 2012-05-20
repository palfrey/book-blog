all: blog_pb2.py

blog_pb2.py: blog.proto
	protoc --python_out=. blog.proto

load::
	python loader.py series.txt series.list

dump::
	python dumper.py series.list series.txt

.PHONY: load dump
