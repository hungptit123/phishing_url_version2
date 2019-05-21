import ipaddress
import re
import requests
import bs4
import urllib.request

def demo(url):
	# html_page = urllib.request.urlopen(url)
	html_page = requests.get(url)
	for x in html_page:
		print (str(x))
		# break
demo("https://viblo.asia/p/tim-hieu-ve-url-va-cach-nhan-biet-link-url-an-toan-3P0lPOonZox")
