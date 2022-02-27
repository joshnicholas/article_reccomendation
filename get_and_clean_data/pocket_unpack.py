import pandas as pd 

df = pd.read_csv('archive/pocket_archive_50.csv')
# 'item_id', 'resolved_id', 'given_url', 'given_title', 'favorite',
# 'status', 'time_added', 'time_updated', 'time_read', 'time_favorited',
# 'sort_id', 'resolved_title', 'resolved_url', 'excerpt', 'is_article',
# 'is_index', 'has_video', 'has_image', 'word_count', 'lang',
# 'time_to_read', 'top_image_url', 'authors', 'image', 'images',
# 'domain_metadata', 'listen_duration_estimate', 'amp_url', 'videos',
# 'tags'

df = df[['status', 'time_added', 'resolved_title', 'resolved_url','excerpt', 'word_count']]

df['time_added'] = pd.to_datetime(df['time_added'], unit="s")
df['time_added'] = df['time_added'].dt.strftime("%Y-%m-%d")

## Preliminary cleaning

df = df.loc[df['resolved_title'].str.len() > 1]
df = df.loc[df['excerpt'].str.len() > 1]
df = df.loc[df['resolved_url'].str.len() > 1]

unread = df.loc[df['status'] == 0].copy()
read = df.loc[df['status'] == 1].copy()

with open('archive/unread.csv', 'w') as f:
       unread.to_csv(f, index=False, header=True)

with open('archive/read.csv', 'w') as f:
       read.to_csv(f, index=False, header=True)

p = read

print(p)
print(p.columns)
