from selenium import webdriver
from bs4 import BeautifulSoup
import time

'''京东商品爬取'''
# 接受用户输入,访问京东
pro = input("请输入要爬取的商品：")
driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe')
driver.get("https://www.jd.com/")
i = 1
# 发送文字到搜索框,点击搜索
text = driver.find_element_by_class_name("text")
text.send_keys(pro)

button = driver.find_element_by_class_name("button")
button.click()
time.sleep(1)

while True:
    # 动态加载-->全部加载
    # 执行脚本,进度条拉到底部
    driver.execute_script(
        'window.scrollTo(0,\
         document.body.scrollHeight)')
    time.sleep(3)
    # 正常解析爬取

    soup = BeautifulSoup(driver.page_source, 'html5lib')
    r_list = soup.select('.goods-list-v2 .gl-item .gl-i-wrap')

    # r为每一个商品的节点对象
    for r in r_list:
        price = r.select_one('.p-price strong i').text.strip()
        name = r.select_one('.p-name-type-2').text.strip()
        shop = r.select_one('.p-shop').text.strip()
        product = dict(name=name, price=price, shop=shop)
        print(product)

    print("第%d页爬取成功" % i)
    i += 1
    # 点击下一页
    if driver.page_source.find("pn-next disabled") == -1:
        driver.find_element_by_class_name("pn-next").click()
        time.sleep(1)
    else:
        print("抓取结束,共抓取%d页" % i)
        break
