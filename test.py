from instapy_cli import client

username = 'doncov-danil@mail.ru' #your username
password = 'ZEg-5q6-6e7-Acx' #your password
image = '/home/mecing/Desktop/Project/posting_bot/1.jpg' #here you can put the image directory
text = 'Here you can put your caption for the post' + '\r\n' + 'you can also put your hashtags #pythondeveloper #webdeveloper'
with client(username, password) as cli:
    cli.upload(image, text)


