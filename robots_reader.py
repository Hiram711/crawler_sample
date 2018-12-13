from urllib import robotparser

rp = robotparser.RobotFileParser()
rp.set_url('https://www.zhihu.com/robots.txt')
rp.read()
print(rp.can_fetch('*', 'https://www.zhihu.com/explore'))
