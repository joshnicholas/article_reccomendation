import feedparser 
import pandas as pd 
from bs4 import BeautifulSoup as bs 

feeds = ['https://www.theguardian.com/australia-news/australian-politics/rss',
'https://www.theguardian.com/environment/climate-change/rss', 
'https://www.theguardian.com/au/business/rss',
'https://www.theguardian.com/au/commentisfree/rss',
'https://www.theguardian.com/world/rss',
'https://www.theguardian.com/au/sport/rss']


url = feeds[0]
count = 1


def grabber(urlo):
    listo = []
    d = feedparser.parse(urlo)
    # 'title', 'title_detail', 'links', 'link', 'summary',
    # 'summary_detail', 'tags', 'published', 'published_parsed',
    # 'id', 'guidislink', 'media_content', 'media_credit', 
    # 'credit', 'authors', 'author', 'author_detail', 'updated', 'updated_parsed'
    print(len(d['entries']))
    for entry in d['entries']:

        title = entry['title']
        published = entry['published']

        summary = bs(entry['summary'], 'html.parser').text
        summary = summary.replace('Continue reading...', '')
        summary = summary.strip()

        link = entry['links'][0]['href']

        data = [{'time_added': published, 
        'resolved_title':title, 
        'resolved_url':link,
        'excerpt':summary}]

        inter = pd.DataFrame.from_records(data)

        listo.append(inter)

    fin = pd.concat(listo)

    return fin

comprie = [grabber(x) for x in feeds]

final = pd.concat(comprie)

final.drop_duplicates(subset=['resolved_title'], inplace=True)

final['time_added'] = pd.to_datetime(final['time_added'])
final['time_added'] = final['time_added'].dt.strftime("%Y-%m-%d")

print(final)

with open('archive/graun.csv', 'w') as f:
    final.to_csv(f, index=False, header=True)

