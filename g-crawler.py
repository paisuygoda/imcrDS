from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

arguments = {"keywords":"sky","limit":3,"print_urls":True, 
			"extract_metadata":True, "no_numbering":True, "delay":True, 
			'save_unknown_format':True, 'output_directory':"pics",
			"no_directory":True
			}
paths = response.download(arguments)
print(paths)