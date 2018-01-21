from django.shortcuts import render
from django.http import HttpResponse
from qablog.models import Article
from datetime import datetime
from django.http import Http404
import paramiko
import sys

def home(request):
    post_list = Article.objects.all()  #获取全部的Article对象
    return render(request, 'home.html', {'post_list' : post_list})

def test(request) :
    return render(request, 'test.html', {'current_time': datetime.datetime.now()})

def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post' : post})

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def ssh_test(request):
    nbytes = 4096
    hostname = '10.184.74.222'
    port = 22
    username = 'daintree'
    password = 'admin'
    command = 'ls -lrt'
    # command = '/opt/daintree/bin/scripts/GetOnOffState.py -g 0022810130520000 -d 0022810210040013 -e 25'

    # client = paramiko.Transport((hostname, port))
    # client.connect(username=username, password=password)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)

    client.connect(hostname, port=port, username=username, password=password,allow_agent=False,look_for_keys=False)
    stdin, stdout, stderr = client.exec_command(command)

    outlines = stdout.readlines()
    resp = ''.join(outlines)

    html = "<html><body>stdout_data is %s.</body></html>" % resp

    # session.close()
    client.close()
    return render(request, 'ssh.html', {'ssh_output': resp})
    #return HttpResponse(html)

def beautiful_mainpage(request):

    return render(request, 'mainpage.html')

def form_process(request):
    request.encoding = 'utf-8'
    if 'SC_Address' in request.GET:
        message = 'SC_Address的内容为: ' + request.GET['SC_Address']
    else:
        message = '你提交了空表单'
    return HttpResponse(message)
