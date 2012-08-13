# -*- coding:utf-8 -*-
import re #정규표현식 라이브러리
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(label='사용자 이름',max_length=30)
    email = forms.EmailField(label='이메일')
    password1 = forms.CharField(
                                label='비밀번호',
                                widget=forms.PasswordInput()
                                )
    password2 = forms.CharField(
                                label='비밀번호(확인)',
                                widget=forms.PasswordInput()
                                )
    
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('비밀번호가 일지하지 않습니다.')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$',username):
            raise forms.ValidationError(
                                        '사용자 이름은 알파벳, 숫자, 밑줄(_)만 가능합니다.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('이미 사용 중인 사용자 이름입니다.')


class WriteForm(forms.Form):
    title=forms.CharField(
                          label='제　　목 ',
                          widget=forms.TextInput(attrs={'size':50,'class':'writebox'})
                          )
    content=forms.CharField(
                            label='내　　용 ',
                            widget=forms.Textarea(attrs={'cols':80,'rows':25,'class':'writebox'})
                            )
    
class ModifyForm(forms.Form):
    s_title='aa'
    title=forms.CharField(
                          label='제　　목 ',
                          widget=forms.TextInput(attrs={'size':50,'class':'writebox','value':s_title})
                          )
    content=forms.CharField(
                            label='내　　용 ',
                            widget=forms.Textarea(attrs={'cols':80,'rows':25,'class':'writebox'})
                            )
    
class SearchForm(forms.Form):
    type=forms.ChoiceField(
                             widget=forms.Select(attrs={'id':'search_selectbox'}),
                             choices=(('title', '제목',),
                                      ('content', '본문',),
#                                      ('user', '글쓴이',)
                                      ),
                             initial='title'
                             )
    query=forms.CharField(
                          label="",
                          widget=forms.TextInput(attrs={'size':32,'id':'search_selectbox'})
                          )

class CommentForm(forms.Form):
    comment=forms.CharField(
                          label='　댓글남기기 ',
                          widget=forms.TextInput(attrs={'size':100,'id':'commentbox'})
                          )