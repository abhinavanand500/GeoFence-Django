from django.shortcuts import render
from django.http import HttpResponse
from mysite.models import Student, Attendance
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from math import sqrt
from datetime import datetime
from django.http import JsonResponse
import json
from django.http import StreamingHttpResponse
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
        contact = Student(name=name, phone=phone, usn=usn, password=password, mac=mac, email=email)
        contact.save()
        messages.success(request, "Your response has been Submitted Successfully. Thank You!")
    return render(request, 'contact.html')

@csrf_exempt
def attendance(request):
    print("hii")
    content = json.loads(request.body)
    print(content)
    var_date = datetime.today().strftime('%Y-%m-%d')

    # Emulator location
    long_coll = 37.421998333333335
    lat_coll = -122.08400000000002

    # college location
    # long_coll=12.9337
    # lat_coll=77.6921

    # home location
    # long_coll = 23.35672372
    # lat_coll = 85.30982892

    usn = content['usn']
    password1 = content['password']
    mac1 = content['mac']
    long = content['long']
    lat = content['lat']
    long1 = float(long)
    lat1 = float(lat)
    print(mac1)
    print(usn,password1,long, lat)
    s = mac1.keys()
    mac2 = '12'
    for i in s :
        mac2 = mac2 + "." + i[1:]
    db = Student.objects.filter(usn=usn, password=password1)
    all = Attendance.objects.filter(date=var_date,usn=usn)
    print("This is all" , all.first())
    if(db):
        dist = sqrt((long_coll - long) ** 2 + (lat_coll - lat) ** 2)
        if(dist<10):
            if(all.first()==None):
                today = Attendance(mac=mac2, usn=usn)
                today.save()
                data = {'message' : 'Marked Your Attendance', 'code' : 'SUCCESS'}
                return JsonResponse(data)
            else:
                data = {'message' : 'Your Attendance is already marked for today', 'code' : 'SUCCESS'}
                return JsonResponse(data)
        else:
            data = {'message' : 'You are outside Geofencing location', 'code' : 'FAILED'}
            return JsonResponse(data)
    else:
        data = {'message' : 'Invalid Username and Password', 'code' : 'FAILED'}
        return JsonResponse(data)

def display(request):
    var_date = datetime.today().strftime('%Y-%m-%d')
    db1 = Student.objects.values()
    print(db1)
    all = Attendance.objects.filter(date=var_date)
    presentcount = len(all)
    totalcount = len(db1)
    params = {'object':all , 'presentCount': presentcount, 'totalCount':totalcount}
    return render(request,'dashboard.html', params)

def about(request):
    return render(request, 'about.html')



