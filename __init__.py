import shutil
import folder_paths
import os

comfy_path = os.path.dirname(folder_paths.__file__)
tk_nodes_path = os.path.join(os.path.dirname(__file__))

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

def setup_js():
    js_dest_path = os.path.join(comfy_path, "web", "extensions", "image-metadata")
    if not os.path.exists(js_dest_path):
        os.makedirs(js_dest_path)

    js_src_path = os.path.join(tk_nodes_path, "js", "image_metadata.js")
    shutil.copy(js_src_path, js_dest_path)
    
setup_js()

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']