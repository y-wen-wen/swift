import base64
import json
import os
from wsgiref import headers

import requests
from django.conf.global_settings import STATICFILES_DIRS
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect

# 登陆
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        request.session['name'] = username
        password = request.POST['password']
        user = test(username,password)
        print(user.status_code)
        if user.status_code == 201:
            request.session["token"]=user.headers.get("X-Subject-Token")
            return HttpResponseRedirect("/yangw0123/container_get/",username)
        else:
            message="请输入正确的用户名和密码"
            return render(request,'login.html',{'message':message})
    return render(request,'login.html')


#获取容器信息到主页面并分页显示：
def coantainer_get(request):
    url2 = "http://192.168.172.23:8080/v1/AUTH_c0f6752deedd4f46a37f0807aae4c822?format=json"
    headers = {}
    headers["X-Auth-Token"] = request.session["token"]
    resp1 = requests.get(url2, headers=headers)
    resp2 = resp1.json()
    # 2.创建一个分页器对象
    resp2 = Paginator(resp1, 7)
    # 3. 创建页面对象Page，每一个page对应的是每一个页面，这个page中包含：
    # page对象有三个属性：
    # a> page.number: 表示当前查询的页码；
    # b> page.object_list: 表示当前页要展示的数据；
    # c> page.paginator: 它就是上面创建的Paginator(user_list, 5)这个对象，无论是哪一页，这个paginator对象始终跟着Page对象；
    try:
        page_number = request.GET.get('page', '1')
        page = resp2.page(page_number)
    except (PageNotAnInteger, EmptyPage, InvalidPage):
        # 如果出现上述异常，默认展示第1页
        page = resp2.page(1)
    return render(request, 'container_main.html', {'page': page})


#连接：
def test(username,password):
    data={
        "auth":{
            "identity":{
                "methods":[
                    "password"
                ],
                "password":{
                    "user":{
                        "domain":{
                            "name":"default"
                        },
                        "name":username,
                        "password":password
                    }
                }
            },
            "scope":{
                "project":{
                    "domain":{
                        "name":"default"
                    },
                    "name":"admin"
                }
            }
        }
    }
    url = "http://192.168.172.23:5000/v3/auth/tokens"
    resp = requests.post(url,data=json.dumps(data))
    return(resp)


#容器主界面：
def container_main(request):
    return render(request, 'container_main.html')


#创建容器：
def container_create(request):
    return render(request, 'container_create.html')
def container_create_1(request):
    if request.method == 'POST':
        name = request.POST['name']
        url2 = "http://192.168.172.23:8080/v1/AUTH_c0f6752deedd4f46a37f0807aae4c822/%s?format=json"%(name)
        headers = {}
        headers["X-Auth-Token"] = request.session["token"]
        resp1 = requests.put(url2, headers=headers)
    return HttpResponseRedirect('/yangw0123/container_success')

#删除容器：
def container_delete(request,name):
    return render(request, 'container_delete.html',{'name':name})
def container_delete_1(request,name):
    a = request.POST.get("yes")
    if a == None:
        url2 = "http://192.168.172.23:8080/v1/AUTH_c0f6752deedd4f46a37f0807aae4c822/%s?format=json"%(name)
        headers = {}
        headers["X-Auth-Token"] = request.session["token"]
        resp1 = requests.delete(url2, headers=headers)
    return HttpResponseRedirect('/yangw0123/container_get')
def container_success(request):
    return render(request, 'container_success.html')


#获取对象列表：
def word_list(request,name):
    url2 = "http://192.168.172.23:8080/v1/AUTH_c0f6752deedd4f46a37f0807aae4c822/%s?format=json" % (name)
    headers = {}
    headers["X-Auth-Token"] = request.session["token"]
    resp1 = requests.get(url2, headers=headers)
    resp2 = resp1.json()
    resp2 = Paginator(resp2, 4)
    try:
        page_number = request.GET.get('page', '1')
        page = resp2.page(page_number)
    except (PageNotAnInteger, EmptyPage, InvalidPage):
        page = resp2.page(1)
    return render(request, 'word_list.html', {'page': page,'name':name})


#查看对象：
def object(request,name,objname):
    url2 = "http://192.168.172.23:8080/v1/AUTH_c0f6752deedd4f46a37f0807aae4c822/%s/%s?format=json" % (name,objname)
    headers = {}
    headers["X-Auth-Token"] = request.session["token"]
    rsp2 = requests.get(url2, headers=headers)
    if rsp2.headers["Content-Type"] == 'text/plain' :
        rsp2.encoding='utf-8'
        contents = rsp2.text
        return render(request, 'object.html', {'contents': contents, 'name': name, 'objname': objname})
    elif rsp2.headers["Content-Type"] == 'image/jpeg' or 'image/png' :
        rsp3 = str(base64.b64encode(rsp2.content), 'utf-8')
        return render(request, 'objectphoto.html', {'contents': rsp3, 'name': name, 'objname': objname})
    else:
        rsp2.encoding='utf-8'
        contents = rsp2.text
        return render(request, 'object.html', {'contents': contents, 'name': name, 'objname': objname})


#删除对象：
def object_delete(request, name,objname):
    return render(request, 'object_delete.html', {'name':name,'objname':objname})
def object_delete_1(request,name,objname):
    a = request.POST.get("yes")
    if a == None:
        url2 = "http://192.168.172.23:8080/v1/AUTH_c0f6752deedd4f46a37f0807aae4c822/%s/%s?format=json"%(name,objname)
        headers = {}
        headers["X-Auth-Token"] = request.session["token"]
        resp1 = requests.delete(url2, headers=headers)
    return HttpResponseRedirect('/yangw0123/word_list/'+name)


#上传对象：
def uploadObject(request,name):
    return render(request, 'uploadObject.html', {'name': name})
def uploadObject_1(request,name):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        fileName = request.FILES.get("object", None)
        if not fileName:
            message="未选择文件，请选择文件后上传！！！"
            return render(request, 'uploadObject.html', {'name': name,'message':message})
        else:
            url2 = "http://192.168.172.23:8080/v1/AUTH_c0f6752deedd4f46a37f0807aae4c822/%s/%s?format=json" % (name,fileName)
            headers = {}
            headers["X-Auth-Token"] = request.session["token"]
            resp1 = requests.put(url2, data=fileName,headers=headers)
            return HttpResponseRedirect('/yangw0123/word_list/' + name)


#下载对象
def downloadObject(request,name,objname):
    return render(request, 'downloadObject.html', {'name': name,'objname':objname})
def downloadObject_1(request,name,objname):
    url2 = "http://192.168.172.23:8080/v1/AUTH_c0f6752deedd4f46a37f0807aae4c822/%s/%s?format=json" % (name, objname)
    headers = {}
    headers["X-Auth-Token"] = request.session["token"]
    resp1 = requests.get(url2,headers=headers)
    resps=resp1.text
    with open(r"C:\Users\Lenovo\Desktop\我爱学习\大三上\工程项目\django_test\下载文件存储\%s" %objname,'w+',encoding='utf-8') as f:
        f.write(resps)
    return HttpResponseRedirect('/yangw0123/word_list/' + name)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if user.status_code == 201:
            request.session["token"]=user.headers.get("X-Subject-Token")
            return HttpResponseRedirect("/helloworld/login_success/")
        else:
            message="请输入正确的用户名和密码"
            return render(request,'login.html',{'message':message})
    return render(request,'login.html')

