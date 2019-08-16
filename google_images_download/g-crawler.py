import os
import pickle
import google_images_download

response = google_images_download.googleimagesdownload()

arguments = {"keywords":"ocean", "limit":3, "extract_metadata":True, 
			"no_numbering":True, "delay":True, 
			'save_unknown_format':True, 'output_directory':"pics",
			"no_directory":True, "size":">800*600"
			}

if os.path.exists('good_set.p'):
	with open('good_set.p', mode='rb') as f:
		good_list = list(pickle.load(f))
	if os.path.exists('searched_set.p'):
		with open('searched_set.p', mode='rb') as sl:
			searched_set = pickle.load(sl)

		remaining_list = []
		for img in good_list:
			if not (img in searched_set):
				remaining_list.append(img)
	else:
		searched_set = set()
		remaining_list = good_list

	with open('img_link.p', mode='rb') as sl:
			img_link = pickle.load(sl)

	for img in remaining_list:
		img_url = img_link[img.split('/')[-1]]
		arguments['similar_images'] = img_url
		paths = response.download(arguments)

else:
	paths = response.download(arguments)

print("Finished!\n")

if os.path.exists('term_dict.p'):
	with open('term_dict.p', mode='rb') as f:
		term_dict = pickle.load(f)
	f = open("term_dict.csv", mode="w")
	for k, v in sorted(term_dict.items(), key=lambda x: -x[1]):
		print(k, v)
		f.write(k + ", " + str(v) + "\n")
	f.close()