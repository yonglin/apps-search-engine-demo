from __future__ import  division
from urllib import urlopen
import re
import nltk 
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.stem.porter import *




def wash_data(desc):
	
	desc = nltk.clean_html(desc)
	## subsititute the <adqwq> with '' which means remove the characters like <asdasda>

	desc = re.sub(r'[^a-zA-Z0-9 ]','',desc)
	## remove non alpha-numeric characters

	tokens = nltk.word_tokenize(desc)
	## tokens
	stopwords = nltk.corpus.stopwords.words('english')
	tokens = [token.lower() for token in tokens if token.lower() not in stopwords]
	tokens = [token for token in tokens if len(token) < 15]
	
	stemmer = PorterStemmer()
	tokens = [stemmer.stem(token) for token in tokens]

	##tokens = set(tokens)
	##tokens = list(tokens)
	return tokens
	## remove the overlapping characters

def get_description_dict(description_table):
	description_dict = dict()
	for item in description_table.items():
		desc_clean = wash_data(item[1])
		description_dict[item[0]] =  desc_clean
	return description_dict

def get_description_table(original_url, url_rule_1, url_rule_2, content_rule, name_rule):
	'''
	We will store the app description in a dictionary like {app_name : app_description}
	'''

	url_table = get_url_table(original_url, url_rule_1, url_rule_2)
	i = 1
	description_table = dict()
	for category in url_table:
		for url in category:
			## we need the English description
			url_en = url + "&hl=en"
			page_content = get_page_content(url_en)
			app_name = get_page_name(page_content, name_rule)
			app_description = get_regular_content(page_content, content_rule)
			description_table[app_name] = app_description[0]
			print i, '\t', app_name
			i += 1


	return description_table



def get_url_table(original_url, url_rule_1, url_rule_2):
	original_page_content = get_page_content(original_url)

	url_list = get_urls(original_page_content, url_rule_1)

	url_table = [get_urls(get_page_content(url), url_rule_2) for url in url_list]

	return url_table

def get_urls(page_content, url_rule):
	raw_urls = get_regular_content(page_content, url_rule)
	raw_urls = set(raw_urls)
	urls = [url[6:-1] for url in raw_urls]
	urls = ['https://play.google.com' + url for url in urls]
	return urls

def get_page_name(page_content, rule=r'<title id=\"main-title\">.*?</title>'):

	raw_page_name = get_regular_content(page_content, rule)
	page_name = raw_page_name[0][23:-38]
	## '<title id="main-title">Android Apps on Google Play</title>'

	return page_name

def get_regular_content(str, rule):
	regular_content = re.findall(rule, str)
	return regular_content


def get_page_content(url):
	
	return urlopen(url).read()













