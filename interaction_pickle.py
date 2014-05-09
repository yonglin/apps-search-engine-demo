from spider import *
from TF_IDF import *
import pickle


## description_table is a python dictionary the key is the name of app and the value is a str 
## which store the description of that app
## in order to computefast, we have computed and stored the description_table in advance
f = open('raw.data', 'rb')
description_table = pickle.load(f)

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

	for i in range(n+1):
		print i, '\t', top_n_list[i]

	start = (raw_input('Do you want to continue searching?\nIf yes, type y\nIf not, type n\n') == 'y')