import hmac
import random
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


# 密码加密
def hmacMd5(s):
    return hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()


# 生成语音播放的结果
def processResult(data):
    s = '您的年龄为' + str(data['age']) + '.'
    print(data['emoji'])
    if data['emoji'] != 'none':
        s += '您的表情为' + str(data['emoji']) + '.'
    else:
        s += '没能检测到您的表情呢，请微笑哦.'
    s += '您的性别为' + str(data['gender']) + '.'
    s += '您的分数为' + str(data['beauty']) + '.'
    if data['glaType'] != 'none':
        s += '您戴眼镜的可能性为' + str(data['glaPoss']) + '.' + \
             '您的眼睛的类型为' + str(data['glaType'])
    else:
        s += '您没戴眼镜的可能性为' + str(data['glaPoss'])
    return s


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
            # 调用加密模块
            password = hmacMd5(password)
            # 登陆状态验证
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
                          {'registerMsg': registerMsg,
                           'userForm': userForm})
        else:
            registerMsg = "注册失败"
            return render(request, 'login.html',
                          {'registerMsg': registerMsg,
                           'userForm': userForm})
    else:
        return render(request, 'login.html',
                      {'registerMsg': registerMsg,
                       'userForm': userForm})


# 退出
@login_required
def myLogout(request):
    logout(request)
    userForm = UserForm()
    return render(request, 'login.html', locals())


# ajax请求处理（视频流dataURL/图片文件dataURL 后台处理）
def processAjax(request):
    data = dict()
    if request.POST:
        data['state'] = "OK"
        dataurl = request.POST.get('dataURL', None)
        count = request.POST.get('count', None)
        # 获取当前用户
        username = request.user.username
        data['username'] = username
        # username = request.session.get('username', None)
        # print("username: ", username)
        index = None

        # 第一次请求，新建类，绑定username，存入类数组UserFaceResArray
        if int(count) == 1:
            # 登入，测试用
            # user = User.objects.get_by_natural_key(username='Test1')
            # login(request, user)
            # 建立用户数据暂存区
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
        # 去除文件头，获取base64格式数据
        base64 = dataurl[23:]
        try:
            fr = FaceRecognition(base64)
            fr.run()
            # 获取当前时间，将setting中配置USE_TZ=True改为False，更改默认时区
            dateTime = datetime.now()

            # 当前已获得的所有数据
            line = [fr.get_age(), fr.get_emoji(), fr.get_sex(),
                    fr.get_beauty(), fr.get_glasses_possibility(),
                    fr.get_glasses_type(), dateTime, dataurl]
            # print(f"line: {line}")
            # 如当前请求所得分数更高，
            # 则更新 存入UserFaceResArray数组中 的该类数据
            if line[3] > UserFaceResArray[index].score:
                UserFaceResArray[index].faceData = line
                UserFaceResArray[index].score = line[3]
        except:
            data['state'] = 'NO'
            import traceback
            traceback.print_exc()
        
        # print(f"UserFaceResArray: {UserFaceResArray[0]}")

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
        # 将测试数据结果传回前端
        data['age'] = UserFaceResArray[index].faceData[0]
        data['emoji'] = UserFaceResArray[index].faceData[1]
        data['gender'] = UserFaceResArray[index].faceData[2]
        data['beauty'] = UserFaceResArray[index].faceData[3]
        data['glaPoss'] = UserFaceResArray[index].faceData[4]
        data['glaType'] = UserFaceResArray[index].faceData[5]
        # 将最优图片url发回
        data['ResponseDataURL'] = UserFaceResArray[index].faceData[7]
        print("Last Result: ", UserFaceResArray[index].faceData[0:7])
        s = processResult(data)
        # 生成本次测试用户音频文件
        TTV = TextToVoice(s, username)
        TTV.getVoice()
        # 返回json数据
        return JsonResponse(data)


# 数据一览页面
@login_required
def history(request):
    username = request.user.username
    return render(request, 'history.html', locals())


# 处理数据一览页面Ajax请求
def processHistory(request):
    data = dict()
    if request.POST:
        user = request.user
        userData = UserInfo.objects.filter(user=user)
        # 按日期排序
        userData = userData.order_by('dateTime')
        age, emoji, gender, beauty, glaPoss, \
        glaType, dateTime, ID = [], [], [], [], [], [], [], []
        for info in userData:
            age.append(int(info.age))
            emoji.append(info.emoji)
            gender.append(info.gender)
            beauty.append(float(info.beauty))
            glaPoss.append(float(info.glaPoss))
            glaType.append(info.glaType)
            dateTime.append(info.dateTime)
            ID.append(int(info.id))
        data['age'] = age
        data['emoji'] = emoji
        data['gender'] = gender
        data['beauty'] = beauty
        data['glaPoss'] = glaPoss
        data['glaType'] = glaType
        data['dateTime'] = dateTime
        data['ID'] = ID
        data['state'] = 'OK'
    else:
        data['state'] = 'NO'
    return JsonResponse(data)


# 获取当前的username请求
def usernameAjax(request, username):
    data = dict()
    # username = request.username
    if not User.objects.filter(username=username):
        data['username'] = "True"
    else:
        data['username'] = "False"
    return JsonResponse(data)


# 排名显示Ajax请求
def showRank(request):
    data = dict()
    if request.POST:
        rankList = []
        # 选出每个用户的历史最高颜值评分
        for user in User.objects.all():
            maxScore = -1.0
            for userInfo in UserInfo.objects.filter(user=user):
                if float(userInfo.beauty) > maxScore:
                    maxScore = userInfo.beauty
            if maxScore != -1.0:
                rankList.append([user.username, maxScore])
        n = len(rankList)
        # print(n)
        # 按研制评分高低排序
        for i in range(0, n - 1):
            for j in range(0, n - i - 1):
                if rankList[j][1] < rankList[j + 1][1]:
                    temp = rankList[j]
                    rankList[j] = rankList[j + 1]
                    rankList[j + 1] = temp
        data['name'] = [i[0] for i in rankList]
        data['score'] = [i[1] for i in rankList]
        data['state'] = "OK"
        return JsonResponse(data)
    else:
        data['state'] = "NO"
        return JsonResponse(data)


# 帮助页面
def help(request):
    username = request.user.username
    return render(request, 'help.html', locals())


# 数据一览页面 数据表格删除Ajax请求
def DeleteUserById(request):
    data = dict()
    if request.POST:
        data['state'] = "OK"
        ID = request.POST.get('id', None)
        # print(ID)
        UserInfo.objects.filter(id=ID).delete()
        user = request.user
        userData = UserInfo.objects.filter(user=user)
        # 按日期时间排序
        userData = userData.order_by('dateTime')
        age, emoji, gender, beauty, glaPoss, \
        glaType, dateTime, ID = [], [], [], [], [], [], [], []
        for info in userData:
            age.append(int(info.age))
            emoji.append(info.emoji)
            gender.append(info.gender)
            beauty.append(float(info.beauty))
            glaPoss.append(float(info.glaPoss))
            glaType.append(info.glaType)
            dateTime.append(info.dateTime)
            ID.append(int(info.id))
        data['age'] = age
        data['emoji'] = emoji
        data['gender'] = gender
        data['beauty'] = beauty
        data['glaPoss'] = glaPoss
        data['glaType'] = glaType
        data['dateTime'] = dateTime
        data['state'] = 'OK'
        data['ID'] = ID
    else:
        data['state'] = 'NO'
    return JsonResponse(data)
