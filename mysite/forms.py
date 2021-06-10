from django import forms
from django.db import models 


class LoginForm(forms.Form):
    username = forms.CharField(
        label='',
        max_length=20,
        widget=forms.TextInput(attrs={ 'type': 'text', 'class': 'fadeIn second', 'placeholder': '英文暱稱', 'autofocus': 'autofocus'})
    )
    password = forms.CharField(
        label='',
        max_length=100,
        widget=forms.PasswordInput(attrs={'type': 'text', 'class': 'fadeIn password', 'placeholder': '密碼', 'required': 'true'})
    )

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='',
        max_length=20,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'fadeIn second', 'placeholder': '英文暱稱', 'autofocus': 'autofocus'})
    )
    password1 = forms.CharField(
        label='',
        max_length=100,
        widget=forms.PasswordInput(attrs={'type': 'text', 'class': 'fadeIn password', 'placeholder': '密碼', 'required': 'true'})
    )
    password2 = forms.CharField(
        label='',
        max_length=100,
        widget=forms.PasswordInput(attrs={'type': 'text', 'class': 'fadeIn password', 'placeholder': '確認密碼', 'required': 'true'})
    )
    rank = forms.CharField(
        label='',
        max_length=10,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'fadeIn third', 'placeholder': '級職', 'required': 'true'})
    )
    name = forms.CharField(
        label='',
        max_length=10,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'fadeIn third', 'placeholder': '姓名', 'required': 'true'})
    )

class DateInput(forms.DateInput):
    input_type = 'date'

class NewExploitReport(forms.Form):
    excute_date = forms.DateField(widget=DateInput)

    target_name = forms.CharField(
        max_length=50,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2', 'autofocus': 'autofocus'})
    )
    target_url = forms.CharField(
        required = False,
        max_length=1000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'})
    )
    target_ip = forms.CharField(
        required = False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    target_port = forms.CharField(
        required = False,
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    target_version = forms.CharField(
        required = False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    weakness = forms.CharField(
        required = False,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', })
    )
    search_time = forms.DateField(widget=DateInput)
    source = forms.CharField(
        required = False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    IC_type = forms.CharField(
        required = False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    excute_location = forms.CharField(
        required = False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    vpn_ip = forms.CharField(
        required = False,
        max_length=20,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'})
    )
    use = forms.CharField(
        required = False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    admin = forms.CharField(
        required = False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    people = forms.CharField(
        required = False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    expected = forms.CharField(
        required = False,
        max_length=1000,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    follow_up = forms.CharField(
        required = False,
        max_length=1000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'})
    )

# class NewInforCollectReport(forms.Form):
#     excute_date = forms.DateField(widget=DateInput)

#     target_name = forms.CharField(
#         max_length=50,
#         widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'})
#     )
#     target_url = forms.CharField(
#         max_length=1000,
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'})
#     )
#     target_ip = forms.CharField(
#         max_length=50,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#     target_port = forms.CharField(
#         max_length=10,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#     target_location = forms.CharField(
#         max_length=50,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#     target_warzone = forms.CharField(
#         max_length=10,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#     weakness = forms.CharField(
#         max_length=20,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#     search_time = forms.DateField(widget=DateInput)

#     vpn_ip = forms.CharField(
#         max_length=20,
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'})
#     )
#     topic = forms.CharField(
#         max_length=50,
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'})
#     )
#     content = forms.CharField(
#         max_length=1000,
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'})
#     )
#     # image = forms.ImageField()
#     follow_up = forms.CharField(
#         max_length=1000,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
