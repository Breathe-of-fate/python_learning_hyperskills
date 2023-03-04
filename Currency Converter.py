import requests

all_currencies = requests.get(f'http://www.floatrates.com/daily/{input().lower()}.json').json()
cache = {'usd': 0, 'eur': 0}

while cur_to_convert := input().lower():
    money = float(input())
    print('Checking the cache...')
    if cur_to_convert not in cache:
        print('Sorry, but it is not in the cache!')
    else:
        print('Oh! It is in the cache!')
    cache[cur_to_convert] = all_currencies[cur_to_convert]['rate']
    print(f'You received {round(money * cache[cur_to_convert], 2)} {cur_to_convert.upper()}.')