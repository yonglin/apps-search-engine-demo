from spider import *
from TF_IDF import *
############################################################
#----> original_url is the main page of application on Google Play
#----> url_rule_1 we will use this regular expression to parse the url addresses of 47 apps categories 
#----> url_rule_2 we will use this regular expression to parse the url addresses of 48 apps for each category
#----> content_rule we will use this regular expression to scrawl the description of each app
#----> name_rule we will use this regular expression to scrawl the name of each app

original_url = 'https://play.google.com/store/apps?hl=en'
url_rule_1 = r'href=\"/store/apps/category/.*?\"'
url_rule_2 = r'href=\"/store/apps/details.[^;]*?\"'
content_rule = r'<div class=\"id-app-orig-desc\">.*?<div class=\"show-more-end\"></div>'
name_rule = r'<title id=\"main-title\">.*?</title>'
###########################################################

## description_table is a python dictionary the key is the name of app and the value is a str 
## which store the description of that app
description_table = get_description_table(original_url, url_rule_1, url_rule_2, content_rule, name_rule)

## since description_table just store the raw data from the web, we use app_desc_table to 
## store the washed data app_desc_table is also a python dictionary. 
## Key is the name of app, and the value is a python List containing the washed tokens of the description
app_desc_table = get_description_dict(description_table)

## TF_table is a nested python dictionary. The key of outer dictionary is the name of each app, 
## the inner dictionary key is the token and the value of the inner dictionary is the TF value
TF_table = get_TF_table(app_desc_table)

## description_list is a nested list storing all the tokens of the descriptions of all 47 * 48 = 2256 apps
description_list = get_description_list(app_desc_table)

start = True
while (start):
## type the query to search apps
	type_query = raw_input("Please describe the application you want by key words: \n")

	## clean the query
	query = wash_data(type_query)

	## get the weighted vector by the TF and IDF
	weighted_vectors = get_query_vector(query, TF_table, description_list)

	## input how many apps you wanna us feedbacking
	n = int(raw_input('Pleas input the number of applications you wish us to feedback: \n'))

	## searching
	top_n_list = top_n_apps(weighted_vectors, n)

	## output the apps names
	print "you might want the following {} applications: \n".format(n)

	for i in range(n):
		print i+1, '\t', top_n_list[i]

	print '\n'
	start = (raw_input('Do you want to continue searching?\nIf yes, type y\nIf not, type n\n') == 'y')
