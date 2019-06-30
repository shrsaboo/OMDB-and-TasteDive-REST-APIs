import json
import requests
import requests_with_caching

def get_movies_from_tastedive(m_name):
    baseurl = "https://tastedive.com/api/similar"
    d = {"q":m_name, "type": "movies", "limit": "5"}
    resp = requests_with_caching.get(baseurl, params=d)
    word_ds = resp.json()
    return word_ds

def extract_movie_titles(dict):
    return [d['Name'] for d in dict['Similar']['Results']]

def get_related_titles(listofmovietitles):
    dup_list = [extract_movie_titles(get_movies_from_tastedive(name)) for name in listofmovietitles]
    L4 = []
    for list in dup_list:
        for name in list:
            if name not in L4:
                L4.append(name)
    return L4

def get_movie_data(title):
    baseurl = "http://www.omdbapi.com/"
    d = {"t":title,"r":"json"}
    resp = requests_with_caching.get(baseurl, params=d)
    return resp.json()

def get_movie_rating(dict):
    for d in dict['Ratings']:
        if d['Source'] == "Rotten Tomatoes":
            return int(d['Value'][:-1])
    return 0

def get_sorted_recommendations(listofmovietitles):
    related_list = get_related_titles(listofmovietitles)
    rotten_tomatoes_rating = {}
    for movie in related_list:
        rotten_tomatoes_rating[movie] = get_movie_rating(get_movie_data(movie))
        
    return sorted(rotten_tomatoes_rating, key = lambda x:(rotten_tomatoes_rating[x],x), reverse = True)
