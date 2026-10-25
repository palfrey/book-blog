.venv/bin/activate:
	uv venv

.PHONY: sync
sync: uv.lock pyproject.toml .venv/bin/activate
	uv sync

.PHONY: pre-commit
pre-commit: sync
	uv run pre-commit run -a

blog_pb2.py: blog.proto .tool-versions
	protoc blog.proto --python_out=. 

setup: sync blog_pb2.py