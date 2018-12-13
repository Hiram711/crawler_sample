from PIL import Image
import tesserocr
import requests

# http://my.cnki.net/elibregister/  中国知网注册页面
# http://my.cnki.net/elibregister/CheckCode.aspx 验证码

r = requests.get('http://my.cnki.net/elibregister/CheckCode.aspx')
with open('recaptcha.jpg', 'wb') as f:
    f.write(r.content)

image = Image.open('recaptcha.jpg')

image = image.convert('L')
threshold = 127
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

image = image.point(table, '1')
image.show()

result = tesserocr.image_to_text(image)
print(result)


