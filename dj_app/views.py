import imp
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.apps import apps
from .models import *
import pdb
import re
from django.contrib import messages
from django.forms.models import model_to_dict
# Create your views here.

def display_data(request):
    data = request.GET.get('table_name')
    action_check = request.GET.get('action_check')
    if not(data):
        app_models = apps.get_app_config('dj_app').get_models()
        app_models = [ele.__name__ for ele in app_models]
        final_models = []
        for ele in app_models:
            upper_div = re.findall('[A-Z][^A-Z]*', ele)
            final_model_name = "_".join([str_ing.lower() for str_ing in upper_div])
            final_models.append(final_model_name)
        return render(request,"data_display.html",{"data":[],"field_info":[],'table_names':final_models,"table_name":''})
    else:
        existed_data = ''
        key_field = ''
        new_s = "".join(word[0].upper()+word[1:] for word in data.split("_"))
        new_table = data
        Model = apps.get_model('dj_app', new_s)
        field_names = [field_name.name for field_name in Model._meta.fields]
        if request.GET.get('table_name') == 'student_address':
            data = Model.objects.values_list().order_by('stu_pin_code')
            key_field = 'stu_pin_code'
            std_pin = request.GET.get('id')
            if std_pin:
                existed_data = StudentAddress.objects.get(stu_pin_code=std_pin)
        elif request.GET.get('table_name') == 'student_branch_details':
            data = Model.objects.values_list().order_by('stu_branch')
            key_field = 'stu_branch'
            std_branch = request.GET.get('id')
            if std_branch:
                existed_data = StudentBranchDetails.objects.get(stu_branch=std_branch)
        else:
            data = Model.objects.values_list().order_by('stu_id')
            key_field = 'stu_id'
            std_id = request.GET.get('id')
            if std_id:
                existed_data = StudentDetails.objects.get(stu_id=std_id)
        app_models = apps.get_app_config('dj_app').get_models()
        app_models = [ele.__name__ for ele in app_models]
        final_models = []
        for ele in app_models:
            upper_div = re.findall('[A-Z][^A-Z]*', ele)
            final_model_name = "_".join([str_ing.lower() for str_ing in upper_div])
            final_models.append(final_model_name)
        std_address = ''
        std_branch = ''
        if request.GET['table_name'] == 'student_details':
            std_address = StudentAddress.objects.all()
            std_branch = StudentBranchDetails.objects.all()
        if action_check == 'edit':
            field_names = model_to_dict(existed_data, fields=field_names)
        return render(request,"data_display.html",{"table_name":new_table,"data":data,"field_info":field_names,'table_names':final_models,'create':True,'address_data':std_address,'branch_data':std_branch,'key_field':key_field,'action_check':action_check,'existed_data':existed_data})

def add_data(request):
    if request.method == "POST":
        print(request.POST)
        if request.GET['table_name'] == 'student_address':
            std_pin = request.POST['stu_pin_code']
            std_state = request.POST['stu_state']
            std_city = request.POST['student_city']
            try:
                StudentAddress.objects.get(stu_pin_code=std_pin)
                messages.success(request,"Record with some of this data already exist")
            except:
                StudentAddress.objects.create(stu_pin_code=std_pin,stu_state=std_state,student_city=std_city)
            # messages.success(request,"Success")
            return redirect(reverse('display_data')+'?table_name=student_address')
        elif request.GET['table_name'] == 'student_branch_details':
            stu_branch = request.POST['stu_branch']
            subjects = request.POST['subjects']
            credits = request.POST['credits']
            try:
                StudentBranchDetails.objects.get(stu_branch=stu_branch)
                messages.success(request,"Record with some of this data already exist")
            except:
                StudentBranchDetails.objects.create(stu_branch=stu_branch,subjects=subjects,credits=credits)
            return redirect(reverse('display_data')+'?table_name=student_branch_details')
        elif request.GET['table_name'] == 'student_details':
            stu_id = request.POST['stu_id']
            stu_name = request.POST['stu_name']
            stu_branch = request.POST['stu_branch']
            stu_pin_code = request.POST['stu_pin_code']
            std_branch_data = StudentBranchDetails.objects.get(stu_branch=stu_branch)
            std_address_data = StudentAddress.objects.get(stu_pin_code=stu_pin_code)
            try:
                StudentDetails.objects.get(stu_id=stu_id)
                messages.success(request,"Record with some of this data already exist")
            except:
                StudentDetails.objects.create(stu_id=stu_id,stu_name=stu_name,stu_branch=std_branch_data,stu_pin_code=std_address_data)
            return redirect(reverse('display_data')+'?table_name=student_details')
    if request.GET['table_name'] == 'student_details':
        std_address = StudentAddress.objects.all()
        std_branch = StudentBranchDetails.objects.all()
        return render(request,"student_address.html",{'table_name':request.GET['table_name'],'address_data':std_address,'branch_data':std_branch})
    return render(request,"student_address.html",{'table_name':request.GET['table_name']})


def edit_table(request):
    if request.method == "POST":
        if request.GET['table_name'] == 'student_address':
            std_pin = request.POST['stu_pin_code']
            std_state = request.POST['stu_state']
            std_city = request.POST['student_city']
            StudentAddress.objects.filter(stu_pin_code=std_pin).update(stu_state=std_state,student_city=std_city)
            return redirect(reverse('display_data')+'?table_name=student_address')
        elif request.GET['table_name'] == 'student_branch_details':
            stu_branch = request.POST['stu_branch']
            subjects = request.POST['subjects']
            credits = request.POST['credits']
            StudentBranchDetails.objects.filter(stu_branch=stu_branch).update(subjects=subjects,credits=credits)
            return redirect(reverse('display_data')+'?table_name=student_branch_details')
        elif request.GET['table_name'] == 'student_details':
            stu_id = request.POST['stu_id']
            stu_name = request.POST['stu_name']
            stu_branch = request.POST['stu_branch']
            stu_pin_code = request.POST['stu_pin_code']
            std_branch_data = StudentBranchDetails.objects.get(stu_branch=stu_branch)
            std_address_data = StudentAddress.objects.get(stu_pin_code=stu_pin_code)
            StudentDetails.objects.filter(stu_id=stu_id).update(stu_name=stu_name,stu_branch=std_branch_data,stu_pin_code=std_address_data)
            return redirect(reverse('display_data')+'?table_name=student_details')
    else:
        if request.GET['table_name'] == 'student_address':
            std_pin = request.GET['id']
            data = StudentAddress.objects.get(stu_pin_code=std_pin)
            return render(request,"student_address.html",{'table_name':request.GET['table_name'],'data':data})
        if request.GET['table_name'] == 'student_branch_details':
            std_branch = request.GET['id']
            data = StudentBranchDetails.objects.get(stu_branch=std_branch)
            return render(request,"student_address.html",{'table_name':request.GET['table_name'],'data':data})
        if request.GET['table_name'] == 'student_details':
            std_address = StudentAddress.objects.all()
            std_branch = StudentBranchDetails.objects.all()
            std_id = request.GET['id']
            data = StudentDetails.objects.get(stu_id=std_id)
        return render(request,"student_address.html",{'table_name':request.GET['table_name'],'address_data':std_address,'branch_data':std_branch,'data':data})
    return render(request,"student_address.html",{'table_name':request.GET['table_name']})