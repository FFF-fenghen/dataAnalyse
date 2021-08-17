import urllib.request
import urllib.parse
import urllib.error
from pprint import pprint

# response = urllib.request.urlopen('http://www.baidu.com/')
# pprint(response.read().decode('utf-8'))


# # 获取一个post响应
# # 超时处理
# try:
#     data = bytes(urllib.parse.urlencode({'hello': 'world'}), encoding='utf-8')
#     response = urllib.request.urlopen('http://httpbin.org/post', data=data, timeout=0.01)
#     pprint(response.read().decode('utf-8'))
# except urllib.error.URLError as e:
#     print('time out')


# # 获取响应头的具体信息
# response = urllib.request.urlopen('http://www.baidu.com')
# print(response.getheader('server'))

#  封装头部信息,假装一个浏览器,以防被识别爬虫

url = 'https://douban.com'
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}
data = bytes(urllib.parse.urlencode({'name': 'archilleus'}),encoding='utf-8')
req = urllib.request.Request(url=url, data=data,headers=header,method='POST')
response = urllib.request.urlopen(req)
# print(response.read().decode('utf-8'))
print(response.getheader('user-Agent'))