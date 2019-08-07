# coding: utf-8

from pixivpy3 import *
import json
from time import sleep
import os
import sys
import random
import shutil

def dl(aapi, image, path, tag_path):
	if not os.path.exists(path+image):
		aapi.download(image, path)
	shutil.copyfile(path+image, tag_path+image)

def single_tag(api, aapi, search_tag, tag_dict):
	print("New tag - " + search_tag +" - Start scraping")
	print("----------------------------------------")

	# 検索から情報取得
	saving_direcory_path = './pixiv_images/' + search_tag + "/"
	dbpath = './pixivDB/'
	imgCount = 1
	pageCount = 1
	if not os.path.exists(saving_direcory_path):
		os.mkdir(saving_direcory_path)
	json_result = aapi.search_illust(search_tag, search_target='exact_match_for_tags',req_auth=True)
	if "next_url" in json_result:
		next_qs = aapi.parse_qs(json_result.next_url)
	else:
		next_qs = False
	whileBreaker = False
	# illust.idを識別したい
	while next_qs:
		print("Scraping page " + str(pageCount) + " (pic #" + str(30 * (pageCount - 1) + 1) + " - " + str(30 * pageCount) + ")")
		pageCount += 1

		for illust in json_result.illusts:
			# タグ統計
			gayIllust = False
			for tag_no in range(0, len(illust.tags)-1):
				if illust.tags[tag_no]['name'] in tag_dict:
					tag_dict[illust.tags[tag_no]['name']] += 1
				else:
					tag_dict[illust.tags[tag_no]['name']] = 1

				if illust.tags[tag_no]['name'] == "ホモ" or illust.tags[tag_no]['name'] == "ゲイ" or illust.tags[tag_no]['name'] == "腐向け":
					gayIllust =True

			# ダウンロード
			if not illust.total_bookmarks > 1000:
				continue
			if illust.type == 'ugoira':
				continue
			if gayIllust:
				continue
			print('Downloading Image ... #' + str(imgCount))
			imgCount += 1
			sleep(1+random.random()*2)
			if illust.page_count == 1:
				dl(aapi, illust.image_urls.large, dbpath, saving_direcory_path)
			else:
				dl(aapi, illust.meta_pages[0].image_urls.large, dbpath, saving_direcory_path)
		print(" ")
		json_result = aapi.search_illust(req_auth=True, **next_qs)
		if "next_url" in json_result:
			next_qs = aapi.parse_qs(json_result.next_url)
			sleep(1+random.random()*2)
		else:
			break

	print("\n\n----------------------------------------")
	f = open("searchedTags", "a+", encoding='utf8')
	f.write(search_tag+"\n")
	f.close()
	return tag_dict


# ログイン処理
api = PixivAPI()
aapi = AppPixivAPI()
api.login("qwerty3600", "159357")
aapi.login("qwerty3600", "159357")

tag_dict = {'sample' : 0}
f = open("nextTagList_adjusted", "r", encoding="utf-8")
for line in f:
	line = line.rstrip('\r\n')
	if line == '':
		continue
	tag_dict=single_tag(api, aapi, line, tag_dict)
f.close()

t = open("searchedTags", "r", encoding='utf8')
searchedTags = {'sample' : 0}
for line in t:
	line = line.rstrip('\r\n')
	searchedTags[line] = 1
t.close()

print('Final Tag Ranking\n')
w = open("relatedTags.csv", "w", encoding="utf-8")
for k, v in sorted(tag_dict.items(), key=lambda x: -x[1]):
	if k in searchedTags:
		continue
	searchedTags[k] = 1
	w.write(k + ", " + v)
	if v < 100:
		break

print("----------------------------------------")
print('Finish!')
