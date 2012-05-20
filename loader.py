from google.protobuf import text_format
from sys import argv
from codecs import open

from blog_pb2 import All

db = All()
text_format.Merge(open(argv[1],"rb","utf-8").read(),db)
open(argv[2],"wb").write(db.SerializeToString())

