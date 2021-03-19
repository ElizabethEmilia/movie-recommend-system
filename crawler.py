import requests
from pyquery import PyQuery as pq

for page in range(10):

    url = 'https://movie.douban.com/top250?start=' + str(25 * page)
    doc = pq(requests.get(url).text)

    for row in doc('.grid_view>li'):
        data = {}
        item = pq(row)
        data['name'] = item.find('.info>.hd>a>span').eq(0).text()
        data['director'] = item.find('.info>.bd>p').text().split('主演')[0]
        data['movietype'] = item.find('.info>.bd>p').eq(0).text().split('/')[-1]
        data['score'] = item.find('.star>span').eq(0).attr('class').split('-')[0].split('rating')[1]
        data['img'] = item.find('.pic>a>img').attr('src')

        res = requests.post('http://127.0.0.1:8000/api/push/', json=data)

