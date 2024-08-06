from aip import AipSpeech
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode, quote


class TextToVoice:
    def __init__(self, text, username):
        self.text = text
        self.username = username
        # self.appID = '20700498'
        # self.ak = 'NQyZBBK0iguamFRkY7x5LmOX'
        # self.sk = 'u6ZvLaT4lMLbzWnKZRXyQY9Fs2IAKj1h'
        self.appID = '103836653'
        self.ak = 'boMxUICHxdP5LO4OdpfAiQyw'
        self.sk = 'lXcJ2ghgZcxQkgwbSWsANoCLADKvgX9C'
        self.TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token?'

    # 获取token，已获取token，使用时无需调用
    def getToken(self):
        params = {'grant_type': 'client_credentials',
                  'client_id': self.ak,
                  'client_secret': self.sk}
        post_data = urlencode(params)
        post_data = post_data.encode('utf-8')

        req = Request(self.TOKEN_URL, post_data)

        f = urlopen(req, timeout=5)
        result_str = f.read()

        # 结果转化为字符
        result_str = bytes.decode(result_str)
        # 转化为字典
        result_str = eval(result_str[:-1])

        return result_str['access_token']

    # 利用百度API得到合成声音
    def getVoice(self):
        # 1.使用在线请求合成语音

        # # 两次编码
        # self.text = quote(quote(self.text))
        # print(self.text)
        #
        # cuidInput = '54-BF-64-0A-A6-FE'
        #
        # token = '24.7852505c794af690f9960c1acdc99d5b.2592000.1596210517.282335-20679887'
        # requestUrl = 'https://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s' % (
        # self.text, cuidInput, token)
        # print(requestUrl)

        # 2.使用sdk合成语音
        client = AipSpeech(self.appID, self.ak, self.sk)
        result = client.synthesis(self.text, 'zh', 1, {'vol': 5, 'per': 0, 'spd': 5, 'pit': 5, })
        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            with open('app\\static\\audio\\{0}.mp3'.format(self.username), 'wb+') as f:
                f.write(result)
            print("转换成功")
        else:
            print(result)

    # 播放所得到的合成语音
    def play(self):
        from playsound import playsound
        # playsound('audio.mp3')
        playsound('{0}.mp3'.format(self.username))


if __name__ == '__main__':
    vP = TextToVoice('我是一个测试文件', "test")
    vP.getVoice()
    vP.play()
