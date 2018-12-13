from bs4 import BeautifulSoup
import re

html = """
<html> <head ><title> The Dormouse's story</title></head>
<body>
<p class ="title" name="dromouse"><b> The Dormouse's story</b></p>
<p class ="story"> Once upon a time there were three little sisters; and their names were
<a href ="http://example.com/elsie" class= "sister" id ="link1">Elsie</a>,
<a href ="http://example.com/lacie" class ="sister" id ="link2">Lacie</a> and
<a href="http://example.com/tillie" class ="sister" id ="link3">Tillie</a> ;
and they lived at the bottom of a well.</p>
<p class ="story "> ... </p>
"""

soup = BeautifulSoup(html, 'html5lib')
print(soup.prettify())

# 节点选择器
# 返回单个节点可直接调用，如果返回列表或生成器则先取出单个然后再调用string或attrs
print(soup.head)
print(soup.head.string)  # 获取文本内容
print(soup.p.attrs['name'])  # 嵌套使用,获取属性值
print(soup.p.contents)  # 获取子节点
print(soup.p.contents[0].parent)  # 获取父节点

# 方法选择器
# find _all(name , attrs , recursive , text , **kwargs)
# find(),与上一个方法相同，但只返回第一个结果
print(soup.find_all('a'))  # 传入name
print(soup.find_all(attrs={'class': 'sister'}))  # 传入attrs
print(soup.find_all('a', class_='sister'))  # 组合简写attrs
print(soup.find_all(text=re.compile('ie')))  # 传入text

# css选择器
# select_one(),与select()方法相同，但只返回第一个结果
print(soup.select('.title')[0].text)
print(soup.select('.story .sister'))
