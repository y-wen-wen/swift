# import re
#
# from django.forms import forms
#
#
# class LoginForm(forms.Form):
#     domain = forms.CharFiled(label="域名" ,max_length=50)
#     username = forms.CharFiled(lable="账号" ,max_length=50)
#     password = forms.CharFiled(lable="密码", max_length=50,widget=3 )
#
#     def clean(self):
#         domain=self.cleaned_data.get("domain")
#         wrongRegex=re.compile('[^a-zA-Z0-9]')
#         if wrongRegex.search(domain)!=None:
#             raise forms.ValidationError("域名只能包含数字和字母，请重新输入！")
#         else:
#             if len(domain)<3 or len(domain)>20:
#                 raise forms.ValidationError("域名只能在3-20之间，请重新输入！")
#             return domain
#     def _clean_username(self):
#         username = self.cleaned_data.get("username")
#         wrongRegex = re.compile('[^a-zA-Z0-9]')
#         if wrongRegex.search(username)!=None:
#             raise forms.ValidationError("账号只能包含数字和字母，请重新输入！")
#         else:
#             if len(username)<3 or len(username)>20:
#                 raise forms.ValidationError("域名只能在3-20之间，请重新输入！")
#             return username
#     def _clean_password(self):
#         password = self.cleaned_data.get("password")
#         wrongRegex = re.compile('[^a-zA-Z0-9]')
#         if wrongRegex.search(password)!=None:
#             raise forms.ValidationError("账号只能包含数字和字母，请重新输入！")
#         else:
#             if len(password)<6 or len(password)>20:
#                 raise forms.ValidationError("密码只能在6-20之间，请重新输入！")
#             return password
