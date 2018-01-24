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
    # request.encoding = 'utf-8'
    # if 'SC_Address' in request.GET:
    #     message = 'SC_Address的内容为: ' + request.GET['SC_Address']
    # else:
    #     message = '你提交了空表单'
    # return HttpResponse(message)

    # The mapping between Clusters and the IDs
    # cluster_dic = {'Basic' : '0', 'Identify' : '3', 'Groups' : '4', 'Scenes' : '5', 'On/Off' : '6', 'Level Control' : '8'}
    cluster_dic = {'0': '0', '1': '3', '2': '4', '3': '5', '4': '6', '5': '8'}
    # attribute_dic = {'ZCLVersion' : '0', 'ManufacturerName' : '4', 'PowerSource' : '7', 'IdentifyTime' : '0',
    #                  'NameSupport' : '0', 'SceneCount' : '0', 'CurrentScene' : '1', 'CurrentGroup' : '2',
    #                  'SceneValid' : '3', 'NameSupport_Scene' : '4', 'OnOff' : '0', 'CurrentLevel' : '0'}
    # Create a dictionary for Attributes. The first dic is for clusters. And the second dic is for attributes.
    attribute_dic = {
                     '0':{
                        '0': '0', # 'ZCLVersion' : '0'
                        '1': '4', # 'ManufacturerName' : '4'
                        '2': '7', # 'PowerSource' : '7'
                     },
                     '1': {
                        '0': '0',  # 'IdentifyTime' : '0'
                     },
                     '2': {
                         '0': '0',  # 'NameSupport' : '0'
                     },
                     '3': {
                         '0': '0',  # 'SceneCount' : '0'
                         '1': '1',  # 'CurrentScene' : '1'
                         '2': '2',  # 'CurrentGroup' : '2'
                         '3': '3',  # 'SceneValid' : '3'
                         '4': '4',  # 'NameSupport_Scene' : '4'
                     },
                     '4': {
                         '0': '0',  # 'OnOff' : '0'
                     },
                     '5': {
                         '0': '0',  # 'CurrentLevel' : '0'
                     },
                     }
    testman_cluster_dic = {'0': 'GenericClusters', '1': 'DimmingLightClusters'}
    testman_suites_dic = {
                         '0': {
                             '0': 'All',
                             '1': '00_profile_wide',
                             '2': '01_basic',
                             '3': '02_identify',
                             '4': '03_commissioning',
                             '5': '04_groups',
                             '6': '11_zdocommands',
                         },
                         '1': {
                             '0': 'All',
                             '1': '05_on_off',
                             '2': '06_level_control',
                             '3': '07_move',
                             '4': '08_ballast',
                             '5': '09_bind_and_reporting',
                             '6': '10_scenes',
                         },
                         }

    nbytes = 4096
    # hostname = '10.184.74.222'
    hostname = request.GET['SC_Address']
    WAC = request.GET['WAC_Address']
    Device_IEEE = request.GET['Device_Address']
    Endpoint = request.GET['Device_Endpoint']
    Cluster = cluster_dic[request.GET['Device_Cluster']]
    Attribute = attribute_dic[request.GET['Device_Cluster']][request.GET['Device_Attribute']]
    Testman_Cluster = testman_cluster_dic[request.GET['TM_Clusters']]
    Testman_Suites = testman_suites_dic[request.GET['TM_Clusters']][request.GET['TM_Suites']]
    port = 22
    username = 'daintree'
    password = 'admin'

    #Parse the command inputed

    if request.GET['Perform_Action'] == 'Read_Attribute':
        command = '/opt/daintree/bin/scripts/ReadAttributes.py -g ' + WAC + ' -d ' + Device_IEEE + ' -e ' + Endpoint + ' -c ' + Cluster + ' -a ' + Attribute
    elif request.GET['Perform_Action'] == 'ReadBindings':
        command = '/opt/daintree/bin/scripts/ReadBindings.py -g ' + WAC + ' -d ' + Device_IEEE + ' -e ' + Endpoint
    elif request.GET['Perform_Action'] == 'GetGroupMembership':
        command = '/opt/daintree/bin/scripts/GetGroupMembership.py -g ' + WAC + ' -d ' + Device_IEEE + ' -e ' + Endpoint
    elif request.GET['Perform_Action'] == 'Identify':
        command = '/opt/daintree/bin/scripts/StartIdentify.py -g ' + WAC + ' -d ' + Device_IEEE + ' -e ' + Endpoint
    elif request.GET['Perform_Action'] == 'GetCurrentLevel':
        command = '/opt/daintree/bin/scripts/GetCurrentLevel.py -g ' + WAC + ' -d ' + Device_IEEE + ' -e ' + Endpoint
    elif request.GET['Perform_Action'] == 'GetIdentifyTime':
        command = '/opt/daintree/bin/scripts/GetIdentifyTime.py -g ' + WAC + ' -d ' + Device_IEEE + ' -e ' + Endpoint
    elif request.GET['Perform_Action'] == 'GetOnOffState':
        command = '/opt/daintree/bin/scripts/GetOnOffState.py -g ' + WAC + ' -d ' + Device_IEEE + ' -e ' + Endpoint
    elif request.GET['Perform_Action'] == 'TurnOn':
        command = '/opt/daintree/bin/scripts/TurnOn.py -g ' + WAC + ' -d ' + Device_IEEE + ' -e ' + Endpoint
    elif request.GET['Perform_Action'] == 'TurnOff':
        command = '/opt/daintree/bin/scripts/TurnOff.py -g ' + WAC + ' -d ' + Device_IEEE + ' -e ' + Endpoint
    elif request.GET['Perform_Action'] == 'ReadReportingConfig':
        command = '/opt/daintree/bin/scripts/ReadReportingConfig.py -g ' + WAC + ' -d ' + Device_IEEE + ' -e ' + Endpoint + ' -c ' + Cluster + ' -a ' + Attribute
    elif request.GET['Perform_Action'] == 'ReadSimpleDescriptor':
        command = '/opt/daintree/bin/scripts/ReadSimpleDescriptor.py -g ' + WAC + ' -d ' + Device_IEEE + ' -e ' + Endpoint

    # For testman
    if request.GET['Perform_Action'] == 'Testman':
        if Testman_Suites == 'All':
            command = '/opt/daintree/bin/automation/testman.py -c system.py -r -t ' + Testman_Cluster + ' third_party'
        else:
            command = '/opt/daintree/bin/automation/testman.py -c system.py -r -t ' + Testman_Cluster + ' third_party' + '/' + Testman_Suites

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
    return render(request, 'ssh.html', {'Device_IEEE': Device_IEEE, 'Endpoint': Endpoint, 'Cluster': Cluster, 'Attribute': Attribute, 'ssh_output': resp})