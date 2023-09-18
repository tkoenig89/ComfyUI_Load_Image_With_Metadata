import torch
import os
import hashlib
import numpy as np
import folder_paths
from .sd_prompt_reader.image_data_reader import ImageDataReader

from PIL import Image, ImageOps

debug = False

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
        image, mask, image_path = self.read_image(image)        
        reader = self.parse_metadata(image_path)

        return self.parse_result(reader, image, mask)

    def read_image(self, image):
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
        return image, mask, image_path

    def parse_metadata(self, image_path):
        reader = ImageDataReader(image_path)
        if(reader.tool == ''):
            raise ValueError('Unable to read generation metadata from image!')
        
        return reader
    
    def parse_result(self, reader: ImageDataReader, image: Image, mask):
        try:        
            seed = int(reader.parameter["seed"])
        except:
            print("Failed to parse seed '{0}'".format(reader.parameter["seed"]))
            seed = 0

        try:
            size = reader.parameter["size"]
            sizeSplit = size.split("x")
            width = int(sizeSplit[0])
            height = int(sizeSplit[1])
        except:
            print("Failed to parse size '{0}'".format(reader.parameter["size"]))
            width = 0
            height = 0

        try:
            cfg = float(reader.parameter["cfg"])
        except:
            print("Failed to parse cfg '{0}'".format(reader.parameter["cfg"]))
            cfg = 0.0     
        
        try:
            steps = int(reader.parameter["steps"])
        except:
            print("Failed to parse steps '{0}'".format(reader.parameter["steps"]))
            steps = 0

        if debug:
            print("Read metadata from image")
            print("Tool: {0}".format(reader.tool))
            print("Positive: {0}".format(reader.positive))
            print("Negative: {0}".format(reader.negative))
            print("Size: {0}x{1}".format(width, height))
            print("Seed: {0}".format(seed))
            print("Cfg: {0}".format(cfg))
            print("Steps: {0}".format(steps))
        
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
