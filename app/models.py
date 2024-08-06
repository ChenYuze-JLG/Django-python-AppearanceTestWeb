from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    # 数据列表样例[22, 'none', 'male', 43.72, 1, 'common', datetime]
    # 年龄
    age = models.IntegerField()
    # 表情：none:不笑；smile:微笑；laugh:大笑
    emoji = models.CharField(max_length=32)
    # 性别：male:男性 female:女性
    gender = models.CharField(max_length=8)
    # beauty最多4位，其中两位小数（本处最大99.99）
    beauty = models.DecimalField(max_digits=4, decimal_places=2)
    # 是否戴眼镜置信度：0~1，需与glassType结合
    glaPoss = models.FloatField()
    # 眼镜类型：none:无眼镜，common:普通眼镜，sun:墨镜
    glaType = models.CharField(max_length=32)
    # 日期时间格式：2020-07-06 11:10:36.191424，datetime.datetime.now获取
    dateTime = models.DateTimeField()
    # 外键为User中的user对象，路径为auth.User
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

# 数据库生成指令
# python manage.py makemigrations
# python manage.py migrate
