"""
Created by Bastelcolor

置き換えが必要な場所は
・ツイッターIDとBotの名前
・CK,CS,AT,ASの部分
・[ログファイルのある場所までのパス]\\log.txt
・BotのツイッターIDを@付きで
・[PNGファイルがあるフォルダまでのパス]
です。

また、元素の画像名はスペースも含めて「 (番号).png」で統一されてる場合の処理をかませてあるのでその都度変えてください。
"""
import tweepy
import random
import sys
import time
import requests
import linecache
import json
import datetime
import re
from PIL import Image
import cv2
import numpy as np
import skimage.util
#APIキー入力
Twitter_ID = "(BotのツイッターID)"
SCREEN_NAME = "(Botの名前)"
CK = "APIKey"
CS = "APIKeySecret"
AT = "AccessToken"
AS = "AccessTokenSecret"
#オブジェクト生成
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)
#元素周期表
element_list = ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ba', 'la', 'ce', 'pr', 'nd', 'pm', 'sm', 'eu', 'gd', 'tb', 'dy', 'ho', 'er', 'tm', 'yb', 'lu', 'hf', 'ta', 'w', 're', 'os', 'ir', 'pt', 'au', 'hg', 'tl', 'pb', 'bi', 'po', 'at', 'rn', 'fr', 'ra', 'ac', 'th', 'pa', 'u', 'np', 'pu', 'am', 'cm', 'bk', 'cf', 'es', 'fm', 'md', 'no', 'lr', 'rf', 'db', 'sg', 'bh', 'hs', 'mt', 'ds', 'rg', 'cn', 'nh', 'fl', 'mc', 'lv', 'ts', 'og']
i = 0
Count = 0
while(i<4):
	try:
#タイムライン習得
		api.mentions_timeline()
		timeline=api.mentions_timeline()
#リプライ習得
		for status in timeline:
			tweetlog = open("[ログファイルのある場所までのパス]\\log.txt", "r" ,encoding = "utf_8")
			replylog = tweetlog.read()
			if(status.text in replylog):
				tweetlog.close()
			else:
				my_reply = status.text
				my_reply = my_reply.lstrip("BotのツイッターIDを@付きで ")
				my_reply = my_reply[0:]
				print (my_reply + " を処理するね！")
#元素化かそうかの確認
				if(my_reply[:3] == "元素化"):
#解析開始
					element_st = str.lower(my_reply[3:])
					element_stlist = list(element_st)
					elem = len(element_stlist)
					process = 0
					img_process = 0
					image_id = []
					error = 0
					for pro in element_stlist:
						if(elem < process+1):
							break
						else:
							if(element_stlist[process] in element_list):
								image_id.append(element_list.index(element_stlist[process])+1)
							elif(error == 1):
								break
							else:
								process_list = element_stlist[process] + element_stlist[process+1]
								if(process_list in element_list):
									image_id.append(element_list.index(process_list)+1)
									process = process + 1
								else:
									print("変換できない文字があったよ・・・")
									error = 1
							process = process + 1
							img_process = img_process + 1
#画像読み込み
					image_number = 0
					element_image = []
					for image in image_id:
						element_image.append(cv2.imread("[PNGファイルがあるフォルダまでのパス] (" + str(image_id[image_number]) + ").png"))
						image_number = image_number + 1
					output_st = ""
					for output_list in image_id:
						output_st = output_st + ",element_image[" + str(output_list) + "] "
					output_st = output_st[1:]
					output_st = "["+output_st+"]"
					
#画像生成
					im_v = cv2.hconcat(element_image)
					cv2.imwrite("[PNGファイルがあるフォルダまでのパス]\\output.jpg", im_v)
#ちゃんと元素化できた場合のリプライ送信
					if(error == 0):
						status_id=status.id
						raw_screen_name=str(status.author.screen_name.encode("UTF-8"))
						screen_name=str(raw_screen_name[2:-1])
						reply_text="@" + screen_name + " 変換できたよ！"
						api.update_with_media(filename = "[PNGファイルがあるフォルダまでのパス]\\output.jpg",status=reply_text,in_reply_to_status_id=status_id)
#再度送信停止のためのログ作成
						replylog = replylog[:-1] +status.text +  "' ]"
						tweetlog = open("[ログファイルのある場所までのパス]\\log.txt", "w" ,encoding = "utf_8")
						tweetlog.write(replylog)
						tweetlog.close()
						print("ログをほぞんしたよ！")
					else:
#元素化できない英語があった場合のリプライ送信
						status_id=status.id
						raw_screen_name=str(status.author.screen_name.encode("UTF-8"))
						screen_name=str(raw_screen_name[2:-1])
						reply_text="@" + screen_name + " ここまでしか変換できなかったよ・・・・"
						api.update_with_media(filename = "[PNGファイルがあるフォルダまでのパス]\\output.jpg",status=reply_text,in_reply_to_status_id=status_id)
#再度送信停止のためのログ作成
						replylog = replylog[:-1] +status.text +  "' ]"
						tweetlog = open("[ログファイルのある場所までのパス]\\log.txt", "w" ,encoding = "utf_8")
						tweetlog.write(replylog)
						tweetlog.close()
						print("ログをほぞんしたよ！")
					
				else:
					raw_screen_name=str(status.author.screen_name.encode("UTF-8"))
					screen_name=str(raw_screen_name[2:-1])
					print(screen_name + "さんは元素化してほしいわけじゃないみたい・・・")
#再度送信停止のためのログ作成
					replylog = replylog[:-1] +status.text +  "' ]"
					tweetlog = open("[ログファイルのある場所までのパス]\\log.txt", "w" ,encoding = "utf_8")
					tweetlog.write(replylog)
					tweetlog.close()
					print("ログをほぞんしたよ！")
#そもそも元素化じゃなかった場合のリプライ送信
					status_id=status.id
					raw_screen_name=str(status.author.screen_name.encode("UTF-8"))
					screen_name=str(raw_screen_name[2:-1])
					reply_text="@" + screen_name + " 元素化 + 変換してほしい英語名\nでリプライを送ってね！"
					api.update_status(status=reply_text,in_reply_to_status_id=status_id)
#レートが早すぎるエラーが発生した時の処理
	except tweepy.TweepError as e:
		if e.reason == "[{'message': 'Rate limit exceeded', 'code': 88}]":
			print(str(e)+" ってエラーが発生したからちょっときゅうけーい！\n")
			time.sleep(60 * 15)
	else:
		#print("処理しゅーりょー！\n")
		error = 0
	time.sleep(60)
	#print("再処理にはいるよ！")
	
	
#ツイート部分コピペ
	"""
	status_id=status.id
	raw_screen_name=str(status.author.screen_name.encode("UTF-8"))
	screen_name=str(raw_screen_name[2:-1])
	print (screen_name)
	reply_text="@" + screen_name + " text"
	api.update_status(status=reply_text,in_reply_to_status_id=status_id)
	"""
