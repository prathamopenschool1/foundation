import os
from pprint import pprint
from zipfile import ZipFile
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import PlayersDatastore, AppsList, FilesRelatedToAppsList
from django.contrib.auth.models import User
from pathlib import Path
import requests
import json


homeDir = str(Path.home())

headers = {
            'cache-control': "no-cache",
            'content-type': "application/json",
            "Accept": "application/json"
        }


# function to fetch programs
def index(request):
    try:
        user_data = User.objects.all()
        if not user_data:
            # fetching programs from server
            programs_urls = "http://swap.prathamcms.org/api/program"
            program_api_response = requests.request('get', programs_urls, headers=headers)
            program_api_result = json.loads(program_api_response.content.decode("utf-8"))
            context = {
                'programs': program_api_result
            }
            return render(request, 'players/setup_index.html', context)
        else:
            return HttpResponseRedirect(reverse('user_login'))
    except Exception as e:
        return HttpResponse("<h2>OOPS!! internet connection not there</h2>", e)


# function to fetch programs after login
@login_required()
def program_call(request):
    # fetching programs from server
    programs_urls = "http://swap.prathamcms.org/api/program"
    program_api_response = requests.request('get', programs_urls, headers=headers)
    program_api_result = json.loads(program_api_response.content.decode("utf-8"))
    context = {
        'programs': program_api_result
    }
    return render(request, 'players/index.html', context)


# function to fetch state
def state_call(request):
    # getting programId from template file
    global program_id
    program_id = ''
    if request.method == 'GET':
        program_id = request.GET.get('program_id')
        # print(program_id)
    # fetching state from server for filling drop down
    state_urls = "http://swap.prathamcms.org/api/state?progid={}" .format(program_id)
    state_api_response = requests.request('get', state_urls, headers=headers)
    state_api_result = json.loads(state_api_response.content.decode("utf-8"))
    # for state in state_api_result:
    #     pprint(state)
    context = {
        "states": state_api_result
    }
    return render(request, 'players/states.html', context)


# function to fetch district
def district_call(request):
    # fetching stateId from template and serving to urls
    global state_id, dist_list, dist_api_result
    state_id = ''
    if request.method == 'GET':
        state_id = request.GET.get('state_id')
    # getting data from server for district
    dist_url = f"http://www.hlearning.openiscool.org/api/village/get?programid={program_id}&state={state_id}"
    dist_api_response = requests.request('get', dist_url, headers=headers)
    dist_api_result = json.loads(dist_api_response.content.decode('utf-8'))
    # pprint(dist_api_result)
    all_villages = dist_api_result
    dist_list = []
    for dist in dist_api_result:
        dist = dist['District']
        dist_list.append(dist)

    unique_dist = set(dist_list)

    context = {
        'districts': unique_dist
    }

    return render(request, 'players/district.html', context)


# fetching block data
def block_call(request):
    # accessing block value from template
    global block_list, district_name
    block_list = set()
    district_name = ''
    if request.method == 'GET':
        district_name = request.GET.get('district_name')
        for block in dist_api_result:
            if district_name == block['District']:
                block_list.add(block['Block'])

    ordered_block_list = set(block_list)  # filtering block list uniquely
    context = {
        'blocks': ordered_block_list
    }

    return render(request, 'players/blocks.html', context)


# getting village list on basis of program, state, district, block
def show_villages(request):
    global village_list, block_name
    block_name = ''

    # list for selected villages
    village_list = []

    if request.method == 'GET':
        block_name = request.GET.get('block_name')
        for selected in dist_api_result:
            if block_name == selected['Block']:
                village_list.append(selected)

    context = {
        'villages': village_list
    }

    return render(request, 'players/villages.html', context)


# fetching and posting all(crl,village,grp,std) data into db
def post_villages(request):
    global village_ids, villages_to_post, grp_api_result, std_api_result, crl_api_result
    if request.method == 'POST':
        village_ids = request.POST.getlist('village_values[]')

    # list for selected village
    villages_to_post = []

    for ids in village_ids:
        for villages in village_list:
            if ids == str(villages['VillageId']):
                villages_to_post.append(villages)
            else:
                continue

    village_key = villages_to_post[0]['VillageId']

    # saving selected village data into db
    village_filter = "programid:" + program_id + ",state:" + state_id
    village_table_data = PlayersDatastore.objects.filter(filter_name=village_filter, table_name='village',
                                                         key_id=str(village_key))
    for datas in village_table_data:
        if datas.table_name and datas.filter_name and datas.key_id:
            datas.delete()
        else:
            continue
    village_data = PlayersDatastore.objects.create(data=villages_to_post, filter_name=village_filter,
                                                   table_name='village', key_id=str(village_key))
    village_data.save()
    # fetching crls data from server
    crl_urls = "http://www.hlearning.openiscool.org/api/crl/get/?programid={}&state={}".format(program_id, state_id)
    crl_api_response = requests.request('get', crl_urls, headers=headers)
    crl_api_result_all = json.loads(crl_api_response.content.decode('utf-8'))

    # saving crls data into db and delete duplicate content
    crl_filter = "programid:" + program_id + ",state:" + state_id
    crl_table_data = PlayersDatastore.objects.filter(table_name='crl', key_id=crl_filter)
    for datas in crl_table_data:
        if datas.table_name and datas.key_id:
            datas.delete()
        else:
            continue
    crl_data1 = PlayersDatastore.objects.create(data=crl_api_result_all, filter_name=crl_filter, table_name='crl',
                                                key_id=crl_filter)
    crl_data1.save()

    # fetching groups from server using village id of selected village
    for ids in villages_to_post:
        ids = ids['VillageId']
        group_url = "http://www.devtab.openiscool.org/api/Group/?programid={}&villageId={}" .format(program_id, ids)
        grp_api_response = requests.request('GET', group_url, headers=headers)
        grp_api_result = json.loads(grp_api_response.content.decode('utf-8'))

        # saving groups data into db according to villageId and programId
        grp_filter = "programid:" + program_id + ",villageid:" + str(ids)
        grp_table_data = PlayersDatastore.objects.filter(table_name='group', key_id=grp_filter)
        for datas in grp_table_data:
            if datas.table_name and datas.key_id:
                datas.delete()
            else:
                continue
        grp_data = PlayersDatastore.objects.create(data=grp_api_result, filter_name=grp_filter, table_name='group',
                                                   key_id=grp_filter)
        grp_data.save()

    # fetching students from server using village id of selected village
    for ids in villages_to_post:
        ids = ids['VillageId']
        std_url = "http://www.devtab.openiscool.org/api/student/?programid={}&villageId={}".format(program_id, ids)
        std_api_response = requests.request('GET', std_url, headers=headers)
        std_api_result = json.loads(std_api_response.content.decode('utf-8'))

        # saving students data into db according to villageId and programId
        std_filter = "programid:" + program_id + ",villageid:" + str(ids)
        std_table_data = PlayersDatastore.objects.filter(table_name='student', key_id=std_filter)
        for datas in std_table_data:
            if datas.table_name and datas.key_id:
                datas.delete()
            else:
                continue
        std_data = PlayersDatastore.objects.create(data=std_api_result, filter_name=std_filter, table_name='student',
                                                   key_id=std_filter)
        std_data.save()

    return HttpResponse("success")

    # return render(request, 'players/post_villages.html')


# fetching crls data from server
def crl_call(request):
    crl_urls = "http://www.hlearning.openiscool.org/api/crl/get/?programid={}&state={}".format(program_id, state_id)
    crl_api_response = requests.request('GET', crl_urls, headers=headers)
    crl_api_result_specific = json.loads(crl_api_response.content.decode('utf-8'))
    # print(crl_api_result_specific, 'crls')
    for i in crl_api_result_specific:
        username = i['UserName']
        password = i['Password']
        email = i['Email']
        first_name = i['FirstName']
        last_name = i['LastName']
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

    return HttpResponse('success')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    user_new = User.objects.all()

    if not user_new:
        return HttpResponseRedirect('/')

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/app_available/')
                else:
                    return HttpResponse('This Account is not active')
            else:
                messages.error(request, 'username or password is not correct')
                return HttpResponseRedirect('/user_login/')

        else:
            return render(request, 'players/login.html', {})


@login_required
def app_available(request):
    global app_list_views
    app_list_views = AppsList.objects.all()
    context = {
        'app_list_views': app_list_views,
    }

    return render(request, 'players/app_available.html', context=context)


@login_required
def apps_list(request):
    global apps_list_result
    apps_list_url = "http://devposapi.prathamopenschool.org/api/AppList"
    apps_list_response = requests.get(apps_list_url, headers=headers)
    apps_list_result = json.loads(apps_list_response.content.decode('utf-8'))
    context = {
        'apps_from_server': apps_list_result,
    }

    return render(request, 'players/apps_list.html', context=context)


def return_json_value(request, pk):
    url_to_convert = "http://devposapi.prathamopenschool.org/api/AppNode?id={}" .format(pk)
    response_url = requests.get(url_to_convert, headers=headers)
    result_url = json.loads(response_url.content.decode('utf-8'))
    context = {
        'json_data': result_url,
    }
    return JsonResponse(context, safe=False)


@login_required
def show_details_of_app(request, pk):
    global all_apps, value
    all_app = []
    detail_url = "http://devposapi.prathamopenschool.org/api/AppNode?id={}" .format(pk)
    detail_response = requests.get(detail_url, headers=headers)
    detail_result = json.loads(detail_response.content.decode('utf-8'))
    for all_apps in apps_list_result:
        for k, v in all_apps.items():
            if v == pk:
                print(all_apps)
                all_app.append(all_apps)

    for value in all_app:
        value = value['AppName']

    print(value)

    context = {
        'detail_result': detail_result,
        'pk': pk,
        'all_app': value,
    }

    return render(request, 'players/show_details.html', context=context)


@login_required
def MasterListByParent(request, pk):
    master_url = "http://devposapi.prathamopenschool.org/Api/AppNodeMasterListByParent?id={}" .format(pk)
    master_response = requests.get(master_url, headers=headers)
    master_result = json.loads(master_response.content.decode('utf-8'))

    context = {
        'master_result': master_result,
    }

    return render(request, 'players/master_list.html', context=context)


def download_and_save(request):
    global node_values, downloadable_file_url, downloadable_file_response, downloadable_file_result, path_to_put

    if request.method == 'POST':
        node_values = request.POST.getlist('node_values[]')

    node_values = list(map(int, node_values))
    print(node_values)

    try:
        for ids in node_values:
            downloadable_file_url = "http://devposapi.prathamopenschool.org/Api/AppNodeDetailListByNode?id=%s" %(ids)
            downloadable_file_response = requests.request('GET', downloadable_file_url, headers=headers)
            downloadable_file_result = json.loads(downloadable_file_response.content.decode('utf-8'))

            pprint(downloadable_file_result)

            for values in downloadable_file_result:
                for j in values['LstFileList']:
                    try:
                        zip_file_url = j['FileUrl']
                        print(zip_file_url, 'zip')
                        print(os.path.basename(zip_file_url), 'base')
                        path_to_put = os.path.join(homeDir, 'zipsandjson')
                        if not os.path.exists(path_to_put):
                            os.makedirs(path_to_put)
                        else:
                            pass
                        path_to_put = os.path.join(path_to_put, str(os.path.basename(zip_file_url)))
                        print(path_to_put)
                        file_to_get = requests.get(zip_file_url)
                        print("ddddd")

                        with open(path_to_put, "wb") as new_zip:
                            for chunk in file_to_get.iter_content(chunk_size=1024):
                                new_zip.write(chunk)

                    except Exception as error:
                        print(error, 'err')
                print(path_to_put, 'oookkk')
                if os.path.exists(path_to_put):
                    NodeId = values['NodeId']
                    NodeType = values['NodeType']
                    NodeTitle = values['NodeTitle']
                    JsonData = values['JsonData']
                    ParentId = values['ParentId']
                    AppId = values['AppId']
                    DateUpdated = values['DateUpdated']
                    app_data = AppsList.objects.create(NodeId=NodeId, NodeType=NodeType, NodeTitle=NodeTitle,
                                                       JsonData=JsonData, ParentId=ParentId,  AppId=AppId,
                                                       DateUpdated=DateUpdated)
                    app_data.save()

                    for files in values['LstFileList']:
                        FileId = files['FileId']
                        NodeId = files['NodeId']
                        FileType = files['FileType']
                        FileUrl = files['FileUrl']
                        DateUpdated = files['DateUpdated']

                        file_data = FilesRelatedToAppsList.objects.create(FileId=FileId, NodeId=NodeId,
                                                                          FileType=FileType, FileUrl=FileUrl,
                                                                          DateUpdated=DateUpdated)

                        file_data.save()

                else:
                    print("No {}".format(path_to_put) + "exists that's why breaking the system")
                    break

        return HttpResponseRedirect('/app_available/')

    except Exception as e:
        print(e)
        return HttpResponse("no internet connection")


@login_required
def update_checker(request, pk):
    global value
    app_date_check = AppsList.objects.get(pk=pk)
    print(app_date_check.DateUpdated)
    app_list_check_url = "http://devposapi.prathamopenschool.org/api/AppNode?id={}" .format(pk)
    apps_list_check_response = requests.get(app_list_check_url, headers=headers)
    apps_list_check_result = json.loads(apps_list_check_response.content.decode('utf-8'))
    # print(apps_list_check_result)
    for apps in apps_list_check_result:
        if app_date_check.NodeTitle == apps['NodeTitle'] and app_date_check.DateUpdated == apps['DateUpdated'] and\
                app_date_check.AppId == apps['AppId']:
            print(apps['NodeTitle'])
            context = {
                'no_update_required': apps,
            }
            return render(request, 'players/app_available.html', context=context)
    else:
        apps_list_url = "http://devposapi.prathamopenschool.org/api/AppList"
        apps_list_response = requests.get(apps_list_url, headers=headers)
        apps_list_result = json.loads(apps_list_response.content.decode('utf-8'))
        all_app = []
        detail_url = "http://devposapi.prathamopenschool.org/api/AppNode?id={}".format(pk)
        detail_response = requests.get(detail_url, headers=headers)
        detail_result = json.loads(detail_response.content.decode('utf-8'))
        for all_apps in apps_list_result:
            for k, v in all_apps.items():
                if v == pk:
                    print(all_apps)
                    all_app.append(all_apps)

        for value in all_app:
            value = value['AppName']

        print(value)

        context = {
            'detail_result': detail_result,
            'pk': pk,
            'all_app': value,
        }

        return render(request, 'players/show_details.html', context=context)