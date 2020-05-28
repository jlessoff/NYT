from nytimesarticle import articleAPI
import time

api = articleAPI('WuHFOtAb5V1If1s5QUJzs1dkOgDYBGgS')
articles = api.search( q = ['NYC','New York'], fq = {'headline':['New York','Connecticut','NYC','New Jersey'], 'source':['Reuters','AP', 'The New York Times']}, begin_date = 20200101, page=1 )

def parse_articles(articles):
    '''
    This function takes in a response to the NYT api and parses
    the articles into a list of dictionaries
    '''
    news = []
    for i in articles['response']['docs']:
        dic = {}
        dic['id'] = i['_id']
        if i['abstract'] is not None:
            dic['abstract'] = i['abstract'].encode("utf8")
        dic['headline'] = i['headline']['main'].encode("utf8")
        dic['desk'] = i['news_desk']
        dic['date'] = i['pub_date'][0:10] # cutting time of day.
        dic['section'] = i['section_name']
        if i['snippet'] is not None:
            dic['snippet'] = i['snippet'].encode("utf8")
        dic['source'] = i['source']
        dic['type'] = i['type_of_material']
        dic['url'] = i['web_url']
        dic['word_count'] = i['word_count']
        # locations
        locations = []
        for x in range(0,len(i['keywords'])):
            if 'glocations' in i['keywords'][x]['name']:
                locations.append(i['keywords'][x]['value'])
        dic['locations'] = locations
        # subject
        subjects = []
        for x in range(0,len(i['keywords'])):
            if 'subject' in i['keywords'][x]['name']:
                subjects.append(i['keywords'][x]['value'])
        dic['subjects'] = subjects
        news.append(dic)
    return(news)

print dict.keys(articles)
all_articles = []
for i in range(1,10): #NYT limits pager to first 100 pages. But rarely will you find over 100 pages of results anyway.
    articles = api.search(q = ['COVID'],
           fq = {'news_desk':['Science'],'source':['Reuters','AP', 'The New York Times']},
           begin_date='20200101',
           end_date='20201231',
           page = str(i))
    articles = parse_articles(articles)
    all_articles = all_articles + articles
    time.sleep(5)
print(all_articles)




    # page=str(i)
    # r = requests.get("http://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date=20100101&q=terrorist+attack&page="+page+"&api-key=***")
    # data = r.json()
    # article = data['response']['docs']
    # for url in article:
    #     print(url["web_url"])

# #
# # #
import csv
keys = all_articles[0].keys()
with open('/Users/jmlessoff/Documents/covid.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_articles)