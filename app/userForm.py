from django import forms
# 导入验证码的Field
from captcha.fields import CaptchaField


# 建立与验证码挂钩的类型
class UserForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码')
    captcha = CaptchaField(label='验证码')



