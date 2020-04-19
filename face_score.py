# baidu_aip
from aip import AipFace
import base64
import urllib
import re


def face_score(link):
    # 图片名称
    pic_name = re.findall(r"public/(.+?)$",link)
    # 图片存储位置
    # 还能巧妙的避免重复!!!
    filePath = '/Users/zhaowenbo/Downloads/crawl_ouban/pictures/'+ pic_name[0]
    # 根据图片的URL获取并保存图片
    urllib.request.urlretrieve(link, filePath)

    # 百度api的一些key
    APP_ID = '18072729'
    API_KEY = 'ZRQcBl5i4f6hlTML09h47vA9'
    SECRET_KEY = 'dimWQ2OhId6Z4AEnpUMdpvuZ4k1se3AR'

    # 使用百度人脸识别API
    aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            content = base64.b64encode(fp.read())
            return content.decode('utf-8')

    imageType = "BASE64"

    options = {}
    options["face_field"] = "age,gender,beauty"

    result = aipFace.detect(get_file_content(filePath),imageType,options)
    # result['result']['face_list'][0]['beauty']   float
    return result['result']['face_list'][0]['beauty']
