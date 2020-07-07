# encoding:utf-8
import requests


class FaceRecognition:
    def __init__(self, base64):
        # print(type(base64))
        self.base64 = base64
        self.result_json = ""
        self.face_list = ""

    def get_result(self):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        params = "{\"image\":\"%s\"," \
                 "\"image_type\":\"BASE64\"," \
                 "\"face_field\":\"age,beauty,expression,face_shape,gender,glasses,landmark,landmark150,r" \
                 "ace,quality,eye_status,emotion,face_type,mask,spoofing\"," \
                 "\"faceshape\":\" \"," \
                 "\"facetype\":\" \"}" % self.base64
        access_token = '24.557b32893a4b59e13ba2941f34153d65.2592000.1596095760.282335-20665916'
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


if __name__ == "__main__":
    fr = FaceRecognition("E:\\py\\black.jpg")
    fr.run()
    print(fr.get_age())
    print(fr.get_emoji())
    print(fr.get_sex())
    print(fr.get_beauty())
    print(fr.get_glasses_possibility())
    print(fr.get_glasses_type())
