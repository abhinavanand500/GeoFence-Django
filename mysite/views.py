from django.shortcuts import render
from django.http import HttpResponse
from mysite.models import Student, Attendance
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
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

    # Emulator location
    # long_coll = 37.421998333333335
    # lat_coll = -122.08400000000002

    # college location
    # long_coll=12.9337
    # lat_coll=77.6921

    # home location
    long_coll = 23.35672372
    lat_coll = 85.30982892

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
    if(db):
        print("Success")
        print(db)
        data = {'message' : 'Marked Your Attendance', 'code' : 'SUCCESS'}
        return JsonResponse(data)




    return render(request, 'contact.html')


def display(request):
    var_date = '"' + datetime.today().strftime('%Y-%m-%d') + '"'
    # mycursor = mydb.cursor()
    # mycursor.execute('SELECT * FROM post_prac2 where created_on=' + var_date)
    # myresult = mycursor.fetchall()
    # var_query = 'SELECT count(*) FROM post_prac2 where created_on=' + var_date
    all = Attendance.objects.filter(usn=usn,)

    # print(var_query)
    mycursor.execute(var_query)
    count = mycursor.fetchall()
    # print(count)

    mycursor.execute('SELECT count(*) FROM signup1')
    signupCount = mycursor.fetchall()
    # print(signupCount)
    return render_template('dashboard.html', text=myresult, presentCount=count, signupCount=signupCount)



def about(request):
    db = Attendance.objects.all().first()
    db1 = Attendance.objects.values()
    for i in db1:
        print(i['date'][0:5])
    context= {'db' : db}
    # print(context.usn)
    return render(request, 'about.html')



