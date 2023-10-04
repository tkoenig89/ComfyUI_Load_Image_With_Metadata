# DISCLAIMER - DISCONTINUED

Please use the [SD Prompt Reader Node](https://github.com/receyuki/comfyui-prompt-reader-node) from now on.

As I made this node, while there was no solution to load metadata in comfy, there is now a nice and comprehensive implementation by the original author of the [SD Prompt Reader](https://github.com/receyuki/stable-diffusion-prompt-reader).
This one also provides a node to save metadata which is much better than anything i tried for this as well. As i don't see any sense in wasting resources on multiple implemetations this repository will not be continued from now on.

# Load Image with metadata

A custom node for comfy ui to read generation data from images (prompt, seed, size...). 
This could be used when upscaling generated images to use the original prompt and seed.

The `Load Image with metadata` is thought as a replacement for the default `Load Image` node.

<img src="./workflow/screenshot.jpg" alt="screenshot" max-height="500"/>

* positive prompt (STRING)
* negative prompt (STRING)
* seed (INT)
* size (STRING: eg. 512x512)
* cfg (FLOAT)
* steps (INT)

# Supported Generators:

* A1111
* EasyDiffusion
* InvokeAI
* NovelAI
* ComfyUI
* DrawThings
* SwarmUI
* Fooocus

# Known Issues

**Comfy UI Images**

As comfy does not store the prompt as actual metadata in the image, the node graph needs to be traversed to find the actual text prompts and other data.
At the moment complex workflows tend to fail resolving the metadata. This is even more complicated with all the custom nodes and different input/output names for text, prompts and conditionings.

# How to use

Find the node via Search `LoadImageWithMetadata` or under `image/LoadImageWithMetadata` in the node dropdown.

# Credits

This is based on a core feature of https://github.com/receyuki/stable-diffusion-prompt-reader.
