import requests
import re

# 基本使用，发起一个get请求
r = requests.get('http://httpbin.org/get')
print(r.text)

# get请求带参数
data = {'name': 'text', 'age': 22}
r = requests.get('http://httpbin.org/get', params=data)
print(r.text)
print(r.json())

# 抓取图片、音频、视频等媒体资源,本质为抓取二进制码
r = requests.get('https://github.com/favicon.ico')
print(r.content)
with open('favicon.ico', 'wb') as f:
    f.write(r.content)

# 添加headersz抓取知乎推荐页面
r = requests.get('https://www.zhihu.com/explore')
print(r.text)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
pattern = re.compile(r'explore-feed.*?question_link.*?>(.*?)</a>', re.S)
r = requests.get('https://www.zhihu.com/explore', headers=headers)
titles = re.findall(pattern, r.text)
print(titles)

# post请求
data = {'name': 'text', 'age': 22}
r = requests.post('http://httpbin.org/post', data=data)

# 获取status_code、cookie等信息
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
r = requests.get('http://www.jianshu.com/', headers=headers)
print(r.status_code)
print(r.cookies)

# 文件上传
files = {'file': open('favicon.ico', 'rb')}
r = requests.post('http://httpbin.org/post', files=files)
print(r.text)

# 读取cookies
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
r = requests.get('https://www.baidu.com/', headers=headers)
print(r.cookies)
for k, v in r.cookies.items():
    print(k + '=' + v)

# 利用cookie保持登录状态,登录知乎后修改cookie再运行
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Host': 'www.zhihu.com',
    'Cookie': '_zap=3578cde4-45ae-459a-a775-6fc420108902; d_c0="AFClegRDNA6PTlyLqhqRdM6aOWnIdAwerPo=|1536805397"; q_c1=c7a25463697d4996a3efd83885e6b673|1544415845000|1539053761000; l_cap_id="ZTBmNjYwMTIwNzY3NDEwNDkyZjE1NWYxNDU0NDU2NjY=|1544426589|4870e7a92ba3091c3a9c32e25e976ff68ff4d126"; r_cap_id="ZWQ5NjJiODAyMTViNGE2NDkyODljOGVhMjQzMDNkNjU=|1544426589|e885d542f4271e9f84f443657b558942a72abaca"; cap_id="ZjVjMzM2N2U5M2EyNDBkYjhhMjg0NzRkOTg2Mjg5MWQ=|1544426589|8a90f1fa0e48994439a152fdf9133f8d3320fcd7"; _xsrf=aGnBtcgWc7yIpNFXCKTkzjXEvEmLm9Bo; __utma=51854390.858720155.1544415868.1544415868.1544426610.2; __utmz=51854390.1544415868.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|3=entry_date=20181009=1; tgw_l7_route=3072ae0b421aa02514eac064fb2d64b5; capsion_ticket="2|1:0|10:1544429916|14:capsion_ticket|44:YzYyNTBlNzA3MWI0NDBiMTk3ZmEzM2JhYWU3ZjA0MDM=|008b7ec426111ee486aa865d76530296ea857821e80a56709f2f387bd32022d6"; z_c0="2|1:0|10:1544429935|4:z_c0|92:Mi4xV3hULUFRQUFBQUFBVUtWNkJFTTBEaVlBQUFCZ0FsVk5iMl83WEFCMGd6TU92WFBHZFg2bEktTnRaZktBVDg5eEJn|6604807de89b747f4614e54b0e438daf729a114318867b9f4125291493846e69"; tst=r'}

r = requests.get('https://www.zhihu.com', headers=headers)
print(True if '我关注的问题' in r.text else False)

# 利用session维持cookie
s = requests.Session()
s.get('http://httpbin.org/cookies/set/number/123456789')
r = s.get('http://httpbin.org/cookies')
print(r.text)

# ssl证书验证
# r = requests.get('https://www.example.com',verify=False) # 不验证证书
# r = requests.get('https://www.example.com', cert='/path/server.pem')  # 单个证书
# r = requests.get('https://www.example.com', cert=('/path/server.crt', '/path/key'))  # crt和key分开

# 超时设置
r = requests.get('http://taobao.com', timeout=1)

# 身份认证
from requests.auth import HTTPBasicAuth

r = requests.get('http://httpbin.org/basic-auth/test/abc123', auth=HTTPBasicAuth('test', 'abc123'))
r = requests.get('http://httpbin.org/basic-auth/test/abc123', auth=('test', 'abc123'))
print(r.status_code)

# Prepared Request
from requests import Request, Session

url = 'http://httpbin.org/post'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
data = {'name': 'text', 'age': 22}
s = Session()
req = Request('POST', url, data=data, headers=headers)
prepared_req = s.prepare_request(req)
s.send(prepared_req)
print(r.text)
