import hmac
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.face import FaceRecognition
from django.http import HttpResponse
from django.http import JsonResponse
from app.data import UserFaceRes, UserFaceResArray
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from app.userForm import UserForm
from app.secretKey import key
from datetime import datetime
from app.models import UserInfo
from django.contrib.auth import authenticate, login, logout
import json

# Create your views here.


# 加密,key为密钥,s为待加密字符串,返回加密结果
from app.voiceAPI import TextToVoice


def hmacMd5(s):
    return hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()


# 主页
@login_required
def index(request):
    username = request.user.username
    return render(request, 'index.html', locals())


# 登录
def myLogin(request):
    msg = "账号或密码输入错误！"
    if request.POST:
        userForm = UserForm(request.POST)
        if userForm.is_valid():  # 验证码正确
            username = userForm.cleaned_data['username']
            password = userForm.cleaned_data['password']
            password = hmacMd5(password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session.set_expiry(0)
                checkBoxList = request.POST.getlist('checkBox')
                if checkBoxList:
                    request.session.set_expiry(10 * 24 * 60 * 60)
                return redirect('/app/index/')
            else:
                return render(request, 'login.html', locals())
        else:
            msg = "验证码错误！"
            return render(request, 'login.html', locals())
    else:
        userForm = UserForm()
        msg = ""
        return render(request, 'login.html', locals())


# 注册用户
def addUser(request):
    registerMsg = ""
    userForm = UserForm()
    if request.POST:
        username = request.POST.get('username1')
        password = request.POST.get('password1')
        print(username, password)
        if not User.objects.filter(username=username):
            password = hmacMd5(password)
            user = User.objects.create_user(username=username, password=password)
            registerMsg = "注册成功"
            return render(request, 'login.html',
                          {'registerMsg': json.dumps(registerMsg),
                           'userForm': userForm})
        else:
            registerMsg = "注册失败"
            return render(request, 'login.html',
                          {'registerMsg': json.dumps(registerMsg),
                           'userForm': userForm})
    else:
        return render(request, 'login.html',
                      {'registerMsg': json.dumps(registerMsg),
                       'userForm': userForm})


# 退出
def myLogout(request):
    logout(request)
    return render(request, 'login.html')


# ajax请求处理
def processAjax(request):
    data = dict()
    if request.POST:
        data['state'] = "OK"
        dataurl = request.POST.get('dataURL', None)
        count = request.POST.get('count', None)
        username = request.user.username
        # username = request.session.get('username', None)
        print("username: ", username)
        index = None

        # 第一次请求，新建类，绑定username，存入类数组UserFaceResArray
        if int(count) == 1:
            # 登入，测试用
            # user = User.objects.get_by_natural_key(username='Test1')
            # login(request, user)

            ufr = UserFaceRes()
            ufr.username = username
            UserFaceResArray.append(ufr)
            index = UserFaceResArray.index(ufr)

        # 获取 目标类item 在 类数组UserFaceResArray 中的下标
        else:
            for item in UserFaceResArray:
                if item.username == username:
                    index = UserFaceResArray.index(item)
        """
        前端发送的dataURL含文件头(data:image/webp;base64,)
        使用前需删除（发回需加回）
        """
        # print(dataurl[:23])
        base64 = dataurl[23:]  # 去头，获取base64格式数据
        try:
            fr = FaceRecognition(base64)
            fr.run()
            # 获取当前时间，将setting中配置USE_TZ=True改为False，更改默认时区
            dateTime = datetime.now()

            # 当前已获得的所有数据
            line = [fr.get_age(), fr.get_emoji(), fr.get_sex(),
                    fr.get_beauty(), fr.get_glasses_possibility(),
                    fr.get_glasses_type(), dateTime, dataurl]

            # 如当前请求所得分数更高，
            # 则更新 存入UserFaceResArray数组中 的该类数据
            if line[3] > UserFaceResArray[index].score:
                UserFaceResArray[index].faceData = line
                UserFaceResArray[index].score = line[3]
        except:
            data['state'] = 'NO'

        # 测量五次后判断，将数据写入数据库
        if int(count) == 5:
            # user = User.objects.get_by_natural_key(username=username)
            UserInfo.objects.create(
                age=UserFaceResArray[index].faceData[0],
                emoji=UserFaceResArray[index].faceData[1],
                gender=UserFaceResArray[index].faceData[2],
                beauty=UserFaceResArray[index].faceData[3],
                glaPoss=UserFaceResArray[index].faceData[4],
                glaType=UserFaceResArray[index].faceData[5],
                dateTime=UserFaceResArray[index].faceData[6],
                user=request.user
            )
            data['age'] = UserFaceResArray[index].faceData[0]
            data['emoji'] = UserFaceResArray[index].faceData[1]
            data['gender'] = UserFaceResArray[index].faceData[2]
            data['beauty'] = UserFaceResArray[index].faceData[3]
            data['glaPoss'] = UserFaceResArray[index].faceData[4]
            data['glaType'] = UserFaceResArray[index].faceData[5]
            # 将最优图片url发回
            data['ResponseDataURL'] = UserFaceResArray[index].faceData[7]
            print("Last Result: ", UserFaceResArray[index].faceData[0:7])
            s = '您的年龄为' + str(data['age']) + ',' + '您的表情为' + str(data['emoji']) \
                + '您的性别为' + str(data['gender']) + '您的分数为' + str(data['beauty']) + \
                '您戴眼镜的可能性为' + str(data['glaPoss']) + '您的眼睛的类型为'
            if data['glaType']:
                s += str(data['glaType'])
            TTV = TextToVoice(s)
            TTV.getVoice()
        # 返回json数据
        return JsonResponse(data)


# 历史数据
def history(request):
    return render(request, 'history.html')


# 处理历史数据Ajax请求
def processHistory(request):
    data = dict()
    if request.POST:
        user = request.user
        userData = UserInfo.objects.filter(user=user)
        userData = userData.order_by('dateTime')
        age, emoji, gender, beauty, glaPoss, \
        glaType, dateTime = [], [], [], [], [], [], []
        for info in userData:
            age.append(int(info.age))
            emoji.append(info.emoji)
            gender.append(info.gender)
            beauty.append(float(info.beauty))
            glaPoss.append(float(info.glaPoss))
            glaType.append(info.glaType)
            dateTime.append(info.dateTime)
        data['age'] = age
        data['emoji'] = emoji
        data['gender'] = gender
        data['beauty'] = beauty
        data['glaPoss'] = glaPoss
        data['glaType'] = glaType
        data['dateTime'] = dateTime
        data['state'] = 'OK'
    else:
        data['state'] = 'NO'
    return JsonResponse(data)
