# %%
import json
from urllib import request 
import requests 
import pandas as pd 
import time 
import random 

perm = 'https://getpocket.com/v3/oauth/request'

app_key = ''

print("App key", app_key)

access_token = ''
headers={'X-Accept': 'application/json'}

# # # %%

# auth_params = {'consumer_key': app_key,
# "redirect_uri":"http://www.google.com"}
# get_key = requests.post(perm, headers=headers, data=auth_params)

# request_token = json.loads(get_key.text)["code"]

# print("Request token: ", request_token)

# # %%
# # print(get_key)
# # print(access_token)

# auth_url = 'https://getpocket.com/auth/authorize'
# print(f"{auth_url}?request_token={request_token}&redirect_uri=http://www.google.com")



# # print(get_key.text) 


# %%

# request_token = ''

# access_token_url = 'https://getpocket.com/v3/oauth/authorize'
# params = {
#     'consumer_key': app_key,
#     'code': request_token,
# }
# headers={'X-Limit-User-Limit': 'application/json'}

# response = requests.post(access_token_url, params=params, headers=headers)

# # print(response.url)
# print(response)
# # print(response.text)
# print(response.headers)
# print(response.status_code)
# print(response.text)

# access_token = response.json()['access_token']

# print("Access token", access_token)


# %%

## Download archive

# old = pd.read_csv('archive/pocket_archive.csv')
old = pd.read_csv('archive/pocket_archive_50.csv')

counter = 1

# for i in range(4770, 12000, 10):
# for i in range(0, 12000, 10):
# for i in range(100, 150, 10):
# for i in range(4760, 4770, 10):
# for i in range(1300, 13000, 50):
for i in range(20000, 25000, 50):
    print("Iteration", counter)
    counter += 1

    wait = random.random() * 5

    auth = {
        'consumer_key': app_key,
        "access_token": access_token,
        'contentType': 'article',
        'sort': "newest",
        'detailType': 'complete',
        'count': 50,
        'offset': i,
        'state': 'all'
    }

    r = requests.get('https://getpocket.com/v3/get', headers=headers, params=auth)

    # print(r.text)
    df = pd.DataFrame(r.json()['list']).transpose()

    old = old.append(df)

    old.drop_duplicates(subset=['item_id'], inplace=True)

    print(old[['resolved_title', 'status']])

    with open('archive/pocket_archive_50.csv', 'w') as f:
        old.to_csv(f, index=False, header=True)
    # with open('archive/pocket_archive_50.csv', 'w') as f:
    #     df.to_csv(f, index=False, header=True)
    
    time.sleep(wait)

