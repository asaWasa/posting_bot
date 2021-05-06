import base64
import requests
import json

api_key = 'f12d0d35fc0f8b72112072cf9e0a8629'


def upload_image(filePath):
    try:
        with open(filePath, "rb") as file:
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": api_key,
                "image": base64.b64encode(file.read()),
            }
            res = requests.post(url, payload)
        if res.status_code == 200:
            print("Server Response: " + str(res.status_code))
            print('data = {}'.format(json.loads(res.text)))
            print("Image Successfully Uploaded")
        else:
            print("ERROR")
            print("Server Response: " + str(res.status_code))
    except FileNotFoundError as e:
        print("FileNotFoundError:", e)

    except OSError as e:
        print("OSError:", e)

    except Exception as e:
        print(type(e), e)


upload_image('/trash/1.jpg')
