from django import forms
from captcha.fields import CaptchaField  # 导入验证码的Field


class UserForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码')
    captcha = CaptchaField(label='验证码')



