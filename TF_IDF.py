from __future__ import  division
from collections import Counter
import numpy as np

def tf(app_desc):
    '''
    tf can compute the TF of any string list
    '''
    tf = dict()
    word_count = len(app_desc)
    ## Counter is a function from collections, which can counter the number of each string in the list
    word_frequency = Counter(app_desc)
    for item in word_frequency.items():
        tf[item[0]] = item[1] / word_count
    return tf

def get_description_list(app_desc_table):
    '''
    description_list is a nested list storing all the tokens of the descriptions of all 47 * 48 = 2256 apps
    '''
    description_list = [descrption for descrption in app_desc_table.values()]

    return description_list


def get_TF_table(app_desc_table):
    '''TF_table is a nested python dictionary. The key of outer dictionary is the name of each app, 
       the inner dictionary key is the token and the value of the inner dictionary is the TF value
    '''
    names = app_desc_table.keys()
    
    TF_table = dict()
    for name in names:
        TF_table[name] = tf(app_desc_table[name])

    return TF_table


def num_apps_containing(word, description_list):
    count = 0
    
    for app_desc in description_list:
        if word in app_desc:
            count += 1
            ## in order to deal with the situation when the word does not appear in any descrption of apps
    return count + 1



def idf(word, description_list):
    '''
    tf can compute the IDF of any word to a list of docs
    '''
    nbr_apps = len(description_list)
    nbr_containing = float(num_apps_containing(word, description_list))
    
    return np.log(nbr_apps / nbr_containing)


def get_query_vector(query, TF_table, description_list):
    '''
    get the weighted vector by the TF and IDF
    '''
    query_TF = tf(query)
    query_IDF = dict()
    query_list = list(set(query))
    for word in query_list:
        query_IDF[word] = idf(word, description_list)
    
    query_vector = [(0.5 + 0.5 * query_TF[word]) * query_IDF[word] for word in query_list]

    app_vector_table = dict()
    
    for name in TF_table.keys():
        app_vector = list()
        for word in query_list:
            try:
                app_vector.append(TF_table[name][word]*query_IDF[word])
            except: 
                app_vector.append(0)
        
        app_vector_table[name] = app_vector

    app_vector_table['query'] = query_vector

    return app_vector_table

def cosine(u, v): 

    length_u = np.sqrt(np.dot(u, u))
    
    length_v = np.sqrt(np.dot(v, v))
    


    if length_u * length_v == 0: 
        cosine = 0 
    else:
        cosine = np.dot(u, v) / (length_u * length_v)
    return cosine


    

def top_n_apps(weighted_vectors, n):
    '''print the top n apps you might want'''
    query = weighted_vectors['query']
    similarity_list = [[name, cosine(query, vector)] for name, vector in weighted_vectors.items()]
    ##similarity_list = list()
    ##for name, vector in weighted_vectors.items():
    ##    similarity_list.append([name,cosine(query,vector)])

    similarity_list = sorted(similarity_list, key=lambda similarity: similarity[1], reverse = True)

    top_n_list = []
    for i in range(n+1):
        if similarity_list[i][0] != 'query':
            top_n_list.append(similarity_list[i][0])

    return  top_n_list