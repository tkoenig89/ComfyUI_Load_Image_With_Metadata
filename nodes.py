import torch
import os
import hashlib
import numpy as np
import folder_paths
from .sd_prompt_reader.image_data_reader import ImageDataReader

from PIL import Image, ImageOps

class LoadImageWithMetadata:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {"image": (sorted(files), )},
                }

    CATEGORY = "image"

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "STRING", "INT", "INT", "INT", "FLOAT", "INT")
    RETURN_NAMES = ("image", "mask", "positive", "negative", "seed", "width","height", "cfg", "steps")
    FUNCTION = "load_image"

    def load_image(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        i = Image.open(image_path)
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
        
        reader = ImageDataReader(image_path)
        #reader.parameter: {'model': 'abc', 'sampler': 'DPM++ 2M Karras', 'seed': '2706265200', 'cfg': '7', 'steps': '25', 'size': '512x512'}
        if(reader.tool == ''):
            raise ValueError('Unable to read generation metadata from image!')

        seed = int(reader.parameter["seed"])
        cfg = float(reader.parameter["cfg"])
        steps = int(reader.parameter["steps"])
        size = reader.parameter["size"]
        sizeSplit = size.split("x")
        width = int(sizeSplit[0])
        height = int(sizeSplit[1])
        
        return (image, mask, reader.positive, reader.negative, seed, width, height, cfg, steps)

    @classmethod
    def IS_CHANGED(s, image):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)

        return True

NODE_CLASS_MAPPINGS = {
    "LoadImageWithMetadata": LoadImageWithMetadata
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImageWithMetadata": "Load Image with metadata"
}
