# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.template import Context
from django.template.loader import get_template
from django.core.context_processors import request
from bbsapp.models import *
from bbsapp.forms import *
from django.template.context import RequestContext
from django.shortcuts import render_to_response
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.timezone import utc
from django.shortcuts import get_object_or_404
import re

@login_required
def list_page(request):
##    try:
#    user=request.user
#    form = SearchForm()
##    except:
##        raise Http404('user불러오기 실패!')
##    lists = List.objects.order_by('id').reverse()
#    lists = List.objects.order_by('-id')    
##    template = get_template('list.html')
#    variables = Context({
#                         'lists':lists,
#                         'user':request.user,
#                         'form':form
#                         })
##    return HttpResponse(template.render(variables))
#    return render_to_response('list.html',variables)
    form = SearchForm()
    lists=[]
    show_results = False
    if request.GET.has_key('query'):
        show_results = True
        query=request.GET['query'].strip()
        if query:
            form=SearchForm({'query':query})
            if request.GET['type']=='content':
                lists = List.objects.filter(content__icontains=query)
            else:
                lists = List.objects.filter(title__icontains=query)
#            lists = List.objects.filter(title__icontains=query,content__icontains=query)[:10]
    else:
            lists = List.objects.order_by('-id')
    variables = RequestContext(request,{'form':form,
                                        'lists':lists,
                                        'user':request.user,
                                        'show_results':show_results,
                                        'show_user':True
                                        })
    return render_to_response('list.html',variables)


@login_required
def view_page(request,id):
#    form = CommentForm()
#    if request.method=='POST':
#        form = CommentForm(request.POST)
#        if form.is_valid():
#            comment = Comment.objects.create(
#                                              comment=form.cleaned_data['comment'],
#                                              parent_id=id,
#                                              user=request.user,
#                                              date=datetime.datetime.utcnow().replace(tzinfo = utc)
#                                              )
#            
#            comment.save()
    view_page=get_object_or_404(
                                List,
                                id=id
                                )
    target = List.objects.get(id=id)
    target.how_many_views +=1
    target.save()
    variables = RequestContext(request,{
                         'view':target,
                         'user':request.user,
                         'view_page':view_page,
                         })
#    variables = RequestContext(request,{
#                                        'view_page':view_page,
#                                        'user':user
#                                        })
#    
    return render_to_response('view.html',variables)

@login_required
def comment_page(request, id):
    user=request.user
    view_page=get_object_or_404(
                                List,
                                id=id
                                )
    variables = RequestContext(request,{
                                        'view_page':view_page,
                                        'user':user
                                        })
    return render_to_response('comment_page.html',variables)

@login_required
def delete_page(request,id):
    user=request.user
    target = List.objects.get(id=id)
    
    if user.username == target.user.username:
        target.delete()
        return HttpResponseRedirect('/bbs/')
    else:
        raise Http404('잘못된 접근입니다. 본인의 게시물만 지울 수 있습니다.')

@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                                            username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            email=form.cleaned_data['email']
                                            )
            return HttpResponseRedirect('/register/success/')
    else:
        form=RegistrationForm()
    
    variables = RequestContext(request, {
                                         'form':form
                                         })
    return render_to_response('registration/register.html',variables)
    
@login_required
def write_page(request):
    if request.method=='POST':
        form = WriteForm(request.POST)
        if form.is_valid():
            list = List.objects.create(
                                              title=form.cleaned_data['title'],
                                              content=form.cleaned_data['content'],
                                              user=request.user,
                                              date=datetime.datetime.utcnow().replace(tzinfo = utc),
                                              how_many_views=0
#                                              date=datetime.datetime.now()
                                              )
            
            list.save()
            return HttpResponseRedirect('/bbs/')
    else:
        form = WriteForm()
    variables=RequestContext(request,{
                                      'form':form,
                                      'state':'글쓰기'
                                      })
    return render_to_response('write.html',variables)

@login_required
def modify_page(request,id):
    list = List.objects.get(id=id)
    if request.method=='POST':
        form = WriteForm(request.POST)
        if form.is_valid():
#            WriteForm.title.widget_attrs(attrs={'size':500,'class':'wrix'})
            list.title=form.cleaned_data['title']
            list.content=form.cleaned_data['content']
            list.date=datetime.datetime.utcnow().replace(tzinfo = utc)
#            list.date=datetime.datetime.now()
            list.save()
            return HttpResponseRedirect('/bbs/'+id)
    else:
        form = WriteForm()
    variables=RequestContext(request,{
                                      'form':form,
                                      'state':'수정'
                                      })
    return render_to_response('write.html',variables)