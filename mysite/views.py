from django.shortcuts import render
from django.http import HttpResponse
from mysite.models import Student, Attendance
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from math import sqrt
from datetime import datetime
from django.http import JsonResponse
import json
import time

# Create your views here.


def home(request):
    return render(request, 'index.html')


def signup(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        phone = request.POST['phone']
        usn = request.POST['usn']
        password = request.POST['password']
        mac = request.POST['mac']
        email = request.POST['email']
        adminp = request.POST['adminp']
        if(adminp == 'iamadmin'):
            contact = Student(name=name, phone=phone, usn=usn,
                              password=password, mac=mac, email=email)
            contact.save()
            messages.success(
                request, "Your response has been Submitted Successfully. Thank You!")
            return render(request, 'contact.html')
        else:
            messages.warning(
                request, "Your admin Password is not correct. This field is strictly for admin")
    return render(request, 'contact.html')


@csrf_exempt
def attendance(request):
    print("hii")
    con = json.loads(request.body)
    print(con['params'])
    content = con['params']
    var_date = datetime.today().strftime('%Y-%m-%d')

    # Emulator location
    long_coll = -122.08400000000002
    lat_coll = 37.421998333333335

    # college location
    # long_coll=12.9337
    # lat_coll=77.6921

    # home location
    # long_coll = 23.35672372
    # lat_coll = 85.30982892

    usn = content['usn']
    password1 = content['password']
    mac1 = content['uq']
    long1 = content['long']
    lat1 = content['lat']
    # long1 = floa(long)
    # lat1 = float(lat)
    curr_time = time.localtime()
    curr_clock = time.strftime("%H:%M:%S", curr_time)
    db = Student.objects.filter(usn=usn, password=password1)
    all = Attendance.objects.filter(date=var_date, usn=usn)
    if(db):
        dist = sqrt((long_coll - long1) ** 2 + (lat_coll - lat1) ** 2)
        print(dist)
        if(dist < 10):
            if(all.first() == None):
                today = Attendance(mac=mac1, usn=usn, time=curr_clock)
                today.save()
                data = {'message': 'Marked Your Attendance', 'code': 'SUCCESS'}
                return JsonResponse(data)
            else:
                data = {
                    'message': 'Your Attendance is already marked for today', 'code': 'SUCCESS'}
                return JsonResponse(data)
        else:
            data = {'message': 'You are outside Geofencing location',
                    'code': 'FAILED'}
            return JsonResponse(data)
    else:
        data = {'message': 'Invalid Username and Password', 'code': 'FAILED'}
        return JsonResponse(data)


def display(request):
    var_date = datetime.today().strftime('%Y-%m-%d')
    db1 = Student.objects.values()
    all = Attendance.objects.filter(date=var_date)
    presentcount = len(all)
    totalcount = len(db1)
    params = {'object': all, 'presentCount': presentcount,
              'totalCount': totalcount}
    return render(request, 'dashboard.html', params)


def about(request):
    return render(request, 'about.html')
