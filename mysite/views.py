from django.shortcuts import render
from django.http import HttpResponse
from mysite.models import Student, Attendance
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from math import sqrt
from datetime import datetime
from django.http import JsonResponse
import json
# Create your views here.
def home(request):
    return render(request, 'index.html')
def signup(request):
    if (request.method == 'POST') :
        name = request.POST['name']
        phone = request.POST['phone']
        usn = request.POST['usn']
        password = request.POST['password']
        mac = request.POST['mac']
        email = request.POST['email']
        adminp = request.POST['adminp']
        if(adminp=='iamadmin'):
            contact = Student(name=name, phone=phone, usn=usn, password=password, mac=mac, email=email)
            contact.save()
            messages.success(request, "Your response has been Submitted Successfully. Thank You!")
            return render(request, 'contact.html')
        else:
            messages.warning(request, "Your admin Password is not correct. This field is strictly for admin")
    return render(request, 'contact.html')
@csrf_exempt
def attendance(request):
    print("hii")
    content = json.loads(request.body)
    print(content)
    now = datetime.now()
    time1 = now.strftime("%H:%M:%S")
    var_date = datetime.today().strftime('%Y-%m-%d')

    # Emulator location
    lat_coll = 37.421998333333335
    long_coll = -122.08400000000002

    # college location
    # lat_coll=12.9337
    # long_coll=77.6921

    # home location
    # lat_coll = 23.35672372
    # long_coll = 85.30982892
    uq = content['uq']
    print("This is uq :: ", uq)
    usn = content['usn']
    password1 = content['password']
    mac1 = content['mac']
    long = content['long']
    lat = content['lat']
    if(usn=='' and password1==''):
        data = {'message' : 'Your Unique Id is :: '+ uq}
        return JsonResponse(data)
    # s = mac1.keys()
    # mac2 = '12'
    # for i in s :
    #     mac2 = mac2 + "." + i[1:]
    print("Hello You are coming out of area")
    db = Student.objects.filter(usn=usn, password=password1)
    all = Attendance.objects.filter(date=var_date,usn=usn)
    if(db):
        dist = sqrt((long_coll - long) ** 2 + (lat_coll - lat) ** 2)
        if(dist<10):
            if(all.first()==None):
                today = Attendance(mac=uq, usn=usn, time=time1, date=var_date)
                today.save()
                data = {'message' : 'Marked Your Attendance'}
                return JsonResponse(data)
            else:
                data = {'message' : 'Your Attendance is already marked for today'}
                return JsonResponse(data)
        else:
            data = {'message' : 'You are outside Geofencing location'}
            return JsonResponse(data)
    else:
        data = {'message' : 'Invalid Username and Password'}
        return JsonResponse(data)

def display(request):
    var_date = datetime.today().strftime('%Y-%m-%d')
    db1 = Student.objects.values()
    all = Attendance.objects.filter(date=var_date)
    print(all.values())
    presentcount = len(all)
    totalcount = len(db1)
    params = {'object':all , 'presentCount': presentcount, 'totalCount':totalcount}
    return render(request,'dashboard.html', params)

def about(request):
    return render(request, 'about.html')



