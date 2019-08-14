from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

arguments = {"keywords":"ocean","limit":1, "extract_metadata":True, 
			"no_numbering":True, "delay":True, 
			'save_unknown_format':True, 'output_directory':"pics",
			"no_directory":True, "related_images":True
			}
paths = response.download(arguments)

print("Finished!")