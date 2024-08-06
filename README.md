conda create -n faceweb python=3.12.4
cd Django-python-AppearanceTestWeb
pip install -r requirements.txt
conda activate faceweb

# 数据库生成指令
python manage.py makemigrations
python manage.py migrate

项目运行命令：
python ./manage.py runserver 0.0.0.0:8000
随后打开 localhost:8000 网址即可使用本项目的功能
示例用户信息：
	- 用户名：Test1
	- 密码：test1

百度人脸检测API文档：https://ai.baidu.com/ai-doc/FACE/yk37c1u4t、
百度智能云控制台-人脸检测：https://console.bce.baidu.com/ai/#/ai/face/overview/index
百度智能云人脸检测在线API测试：https://console.bce.baidu.com/support/?u=dhead#/api?product=AI&project=%E4%BA%BA%E8%84%B8%E8%AF%86%E5%88%AB&parent=%E4%BA%BA%E8%84%B8%E5%9F%BA%E7%A1%80API&api=rest%2F2.0%2Fface%2Fv3%2Fdetect&method=post

百度语音合成API文档：https://cloud.baidu.com/doc/SPEECH/s/mlbxh7xie
百度智能云控制台-语音合成：https://console.bce.baidu.com/ai/#/ai/speech/app/list
百度智能云语音合成在线API测试：https://console.bce.baidu.com/support/#/api?product=AI&project=%E8%AF%AD%E9%9F%B3%E6%8A%80%E6%9C%AF&parent=%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90&api=rpc%2F2.0%2Ftts%2Fv1%2Fcreate&method=post