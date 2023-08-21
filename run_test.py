import sys
import os

# __package__ = 'test'
# sys.path.append(os.getcwd() + '/..')

# sys.path.append('../..')

from nodes import LoadImageWithMetadata

node = LoadImageWithMetadata()

res = node.load_image(".png")

print(res)