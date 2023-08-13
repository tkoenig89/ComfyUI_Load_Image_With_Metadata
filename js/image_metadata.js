import { app } from "/scripts/app.js";

// Adds an upload button to the nodes

app.registerExtension({
	name: "image_meta.UploadImage",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "LoadImageWithMetadata") {
			nodeData.input.required.upload = ["IMAGEUPLOAD"];
		}
	},
});