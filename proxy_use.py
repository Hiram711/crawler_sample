import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# requests代理的使用
proxies = {'http': 'http://118.190.95.35:9001'}
r = requests.get('http://httpbin.org/ip')
print(r.text)
r = requests.get('http://httpbin.org/ip', proxies=proxies)
print(r.text)

# selenium chrome代理
options = Options()
options.add_argument('--proxy-server=http://118.190.95.35:9001')
driver = webdriver.Chrome(chrome_options=options, executable_path=r'D:\chromedriver_win32\chromedriver.exe')
driver.get('http://httpbin.org/ip')
print(driver.page_source)
driver.quit()
