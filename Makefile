blog_pb2.py: blog.proto
	protoc blog.proto --python_out=. 
