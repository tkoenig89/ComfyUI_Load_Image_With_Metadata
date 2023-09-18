import sys
import os

__package__ = 'test'
# sys.path.append(os.getcwd() + '/..')

# sys.path.append('../..')
if __name__ == '__main__':
    from nodes import LoadImageWithMetadata

node = LoadImageWithMetadata()

_,_,*res = node.load_image(".png")

print(res)