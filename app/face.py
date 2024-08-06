# encoding:utf-8
import os
import requests
import json
import base64
import urllib


# 人脸识别封装模块
class FaceRecognition:
    def __init__(self, base64):
        # print(type(base64))
        # base64格式图片数据
        # self.base64 = self.get_file_content_as_base64(base64)
        self.base64 = base64
        self.result_json = ""
        self.face_list = ""

    # 向百度API发送测试、获取数据请求
    def get_result(self):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        params = "{\"image\":\"%s\"," \
                 "\"image_type\":\"BASE64\"," \
                 "\"face_field\":\"age,beauty,expression,face_shape,gender,glasses,landmark,landmark150,r" \
                 "ace,quality,eye_status,emotion,face_type,mask,spoofing\"," \
                 "\"faceshape\":\" \"," \
                 "\"facetype\":\" \"}" % self.base64
        access_token = '24.9e3041a2f74ce73098373992107aca05.2592000.1725531765.282335-103762223'
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            # print(json.dumps(response.json(), indent=4))
            self.result_json = response.json()
            self.face_list = self.result_json['result']['face_list']
            # print(self.face_list)

    def run(self):
        # self.get_base64str()
        self.get_result()

    def get_age(self):
        return self.face_list[0]['age']

    # 返回 male 或 female
    def get_sex(self):
        return self.face_list[0]['gender']['type']

    def get_emoji(self):
        return self.face_list[0]['expression']['type']

    # 返回戴眼镜的置信度(0-1)
    def get_glasses_possibility(self):
        return self.face_list[0]['glasses']['probability']

    # 返回戴眼镜的置信度(0-1)
    def get_glasses_type(self):
        return self.face_list[0]['glasses']['type']

    def get_beauty(self):
        return self.face_list[0]['beauty']


# 本地测试
def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


if __name__ == "__main__":
    imgbase64 = get_file_content_as_base64("./app/static/images/black.jpg")
    fr = FaceRecognition(imgbase64)
    fr.run()
    print(fr.get_age())
    print(fr.get_emoji())
    print(fr.get_sex())
    print(fr.get_beauty())
    print(fr.get_glasses_possibility())
    print(fr.get_glasses_type())
