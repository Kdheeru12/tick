from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile,Users,Challenge,Post
import random
from django.utils import timezone
import requests
from django.db import models
from .models import Video
from .form import ProfileForm,ChallengeForm,PostForm
import shutil
from datetime import datetime
from django.core.mail import send_mail,BadHeaderError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def homepage(request):
    if request.user.is_authenticated:
        users = Profile.objects.all().count()
        challenges = Challenge.objects.all().count()
        print(users)
        context={
            'users':users,
            'challenges':challenges,
        }


        return render(request,'index.html',context)
    else:
        return redirect('/signin')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        date =request.POST['date']
        mobile = request.POST['mobile']
        gender = request.POST['gender']
        globals()['first_name']=first_name
        globals()['last_name']=last_name
        globals()['email'] = email
        globals()['password']= password
        globals()['date']= date
        globals()['mobile']= mobile
        globals()['gender']= gender
        from datetime import date 
        today = date.today() 
        #age = today.year - year - ((today.month, today.day) < (month, date)) 
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email Already exist')
            return redirect('signup')
        else:
            print('aaa')
            import urllib.request
            import urllib.parse
            otp = random.randint(100000,999999)
            globals()['otp']=otp
            def sendSMS(apikey, numbers, sender, message):
                params = {'apikey':'fJfBJnyz91c-TbqrXa8U1yvh9RFUFlIIypeUFJkyJN', 'numbers': numbers, 'message' : message, 'sender': sender}
                f = urllib.request.urlopen('https://api.textlocal.in/send/?'
                    + urllib.parse.urlencode(params))
                return (f.read(), f.code)

            resp, code = sendSMS('fJfBJnyz91c-TbqrXa8U1yvh9RFUFlIIypeUFJkyJN',  str(mobile),
                'TXTLCL', 'hello user otp for verification is "'+str(otp)+'" ')
            print (resp)
            return redirect('verification')
        return render(request,'register.html')
    else:
        return render(request,'register.html')
# Create your views here.
def verification(request):
    if request.method == 'POST':
        try:
            email_otp = int(request.POST['otp'])
            user=User.objects.filter(email=email).exists()
            print(otp)
            otp is not None
        except:
            return redirect('signup')
        print(user)
        if email_otp == (otp or 123456) and user == False:
            import json
            import requests
            res = requests.get('https://ipinfo.io/')
            data = res.json()
            print(data)
            city = data['city']
            location = data['loc'].split(',')
            latitude = location[0]
            longitude = location[1]
            latitude = float(latitude)
            state = data['region']
            messages.info(request,'otp verified')
            user = User.objects.create_user(username=email,password=password,email=email,first_name=first_name,last_name=last_name)
            user_profile = Profile(user=email,firstname=first_name,lastname=last_name,gender=gender,Mobile=mobile,date=date,city=city,lat=latitude,lon=longitude,state=state,address=str(city)+str(state)+str('INDIA'))
            user.save()
            user_profile.save()
            return redirect('login')
        elif user == True:
            messages.info(request,'user already verified')
            return redirect('/signin')
        else:
            messages.info(request,'otp invalid')
            return redirect('verification')
    else: 
        context= {
            "mobile":mobile
            }
        return render(request,'verification.html',context)
def login(request):
    if request.method == 'POST':
        password = request.POST['password']
        email = request.POST['email']
        user = auth.authenticate(username=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,'invalid phone or password')
            return redirect('/signin')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request,'login.html')
def profile(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile,user=str(request.user))
        print(profile)
        instance = get_object_or_404(Profile,user=str(request.user))

        context={
            'profile':profile,
        }
        return render(request,'profile.html',context)
    else:
        return redirect('/signin')
def profileedit(request):
    if request.user.is_authenticated:
        instance = get_object_or_404(Profile,user=str(request.user))
        form = ProfileForm(request.POST or None,request.FILES or None,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('/profile')
        context={
            'form':form
        }
        return render(request,'profile-edit.html',context)
    else:
        return render(request,'profile.html')
def feed(request):
    challenge = Post.objects.all()
    print(challenge)
    context = {
        "Posts":challenge
    }
    return render(request,'feed.html',context) 
def posts(request):
    challenge = Post.objects.filter(user=request.user)
    print(challenge)
    context = {
        "Posts":challenge
    }
    return render(request,'posts.html',context)
def postscreate(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            import json
            import requests
            res = requests.get('https://ipinfo.io/')
            data = res.json()
            city = data['city']
            location = data['loc'].split(',')
            latitude = location[0]
            longitude = location[1]
            latitude = float(latitude)
            import socket    
            hostname = socket.gethostname()    
            IPAddr = socket.gethostbyname(hostname)  
            instance.lat = latitude
            instance.lon = longitude
            instance.location = location
            instance.ip = IPAddr
            instance.slug1 = str(instance.challenge)+str(timezone.now())
            instance.save()
        return redirect('/posts')
    else:

        challenge = Challenge.objects.raw('select id,end_date from challenge where end_date between 2020-08-10 and 2021-12-20 ')
        for i in challenge:
            print(i.end_date)
        form = PostForm()
        print(form)
        context = {
            "form":form,
        }
        return render(request,'posts-create.html',context)
def challenge(request):
    challenge = Challenge.objects.filter(user=request.user)
    print(challenge)
    context = {
        "Challenge":challenge
    }
    return render(request,'challenge.html',context)
def createchallenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST,request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            import json
            import requests
            res = requests.get('https://ipinfo.io/')
            data = res.json()
            city = data['city']
            location = data['loc'].split(',')
            latitude = location[0]
            longitude = location[1]
            latitude = float(latitude)
            import socket    
            hostname = socket.gethostname()    
            IPAddr = socket.gethostbyname(hostname)  
            instance.lat = latitude
            instance.lon = longitude
            instance.location = location
            instance.ip = IPAddr
            instance.save()
        return redirect('/challenge')
    else:
        print(request.user)
        form = ChallengeForm()
        context = {
            "form":form,
        }
        return render(request,'challenge-create.html',context)
def allchallenges(request):
    if request.user.is_authenticated:
        challenge = Challenge.objects.all()
        context = {
            "Challenge":challenge
        }
        return render(request,'allchallenges.html',context)
def logout(request):
    auth.logout(request)
    return redirect('homepage')
def settings(request):
    if request.user.is_authenticated:
        instance = get_object_or_404(Profile,user=str(request.user))
        context={
                'instance':instance,
            }
        return render(request,'settings.html',context)
    else:
        return redirect('/')
def teachers(request):
    if request.method == 'POST':
        name = request.POST['name']
        clas = request.POST['class']
        mobile = request.POST['mobile']
        email = request.POST['email']
        teacher = Teacher.objects.filter(teacher_name=name,teacher_class=clas,teacher_mobile=mobile,teacher_email=email)
        teacher.delete()
        return redirect('/teachers')
    else:
        teacher = Teacher.objects.all()
        print(teacher)
        return render(request,'teachers.html',{'teacher':teacher})
def teachersadd(request):
    if request.method == 'POST': 
        name = request.POST['name']
        clas = request.POST['class']
        mobile = request.POST['mobile']
        email = request.POST['email']
        landline = request.POST['landline']
        aboutme = request.POST['aboutme']
        teacher = Teacher(teacher_name=name,teacher_class=clas,teacher_mobile=mobile,teacher_email=email,teacher_landline=landline,teacher_about_me=aboutme)
        teacher.save()
        return redirect('/teachers')
    else:
        clas = Class.objects.all()
        return render(request,'teachers-add.html',{'clas':clas})
def Classes(request):
    if request.method == 'POST':
        name = request.POST['name']
        clas = request.POST['class']
        section = request.POST['section']
        print(clas,section,name)
        Clas = Class.objects.filter(Class_name=clas,Class_section=section)
        print(clas)
        Clas.delete()
        return redirect('/classes')
    else:
        clas = Class.objects.all()
        return render(request,'classes.html',{'clas':clas})
def Classesadd(request):
    if request.method == 'POST':
        name = request.POST['name']
        section = request.POST['section']
        clas = Class(Class_name=name,Class_section=section)
        clas.save()
        studentcount = Students.objects.filter(student_section=section,student_class=clas).count()
        instance = get_object_or_404(Class,Class_name=clas,Class_section=section)
        instance.Class_size = int(studentcount)
        instance.save()
        return redirect('/classes')
    else:
        teacher = Teacher.objects.all()
        return render(request,'classes-add.html',{'teacher':teacher})
def students(request):
    if request.method == 'POST':
        name = request.POST['name']
        clas = request.POST['class']
        section = request.POST['section']
        students = Students.objects.filter(student_class=clas,student_name=name,student_section=section)
        students.delete()
        studentcount = Students.objects.filter(student_section=section,student_class=clas).count()
        instance = get_object_or_404(Class,Class_name=clas,Class_section=section)
        instance.Class_size = int(studentcount)
        instance.save()
        return redirect('/students')
    else:
        students = Students.objects.all() 
        return render(request,'students.html',{'students':students})
def studentsadd(request):
    if request.method == 'POST':
        name = request.POST['name']
        clas = request.POST['class']
        mobile = request.POST['number']
        email = request.POST['email']
        section = request.POST['section']
        students = Students(student_name=name,student_section=section,student_class=clas,student_mobile=mobile)
        students.save()
        studentcount = Students.objects.filter(student_section=section,student_class=clas).count()
        instance = get_object_or_404(Class,Class_name=clas,Class_section=section)
        instance.Class_size = int(studentcount)
        instance.save()
        return redirect('/students')
    clas = Class.objects.all()
    return render(request,'students-add.html',{'clas':clas})
def usersadd(request):
    if request.method=='POST':
        name = request.POST['name']
        mobile =request.POST['mobile']
        gender = request.POST['gender']
        lat =request.POST['lat']
        lon =request.POST['lon']
        location = request.POST['location']
        age = request.POST['age']
        intrests = request.POST['intrests']
        use = Users(name=name,mobile=mobile,gender=gender,age=age,lat=lat,lon=lon,intrests=intrests,location=location)
        use.save()
        return redirect('/')
    else:
        import json
        import requests
        res = requests.get('https://ipinfo.io/')
        data = res.json()
        print(data)
        city = data['city']
        location = data['loc'].split(',')
        latitude = location[0]
        longitude = location[1]
        latitude = float(latitude)
        state = data['region']
        longitude = float(longitude)
        globals()['latitude']= latitude
        globals()['longitude']= longitude
        print("Latitude : ", latitude)
        print("Longitude : ", longitude)
        print("City : ", state)
        context = {
            'lat':latitude,
            'lon':longitude,
            'city':city,
            'state':state,
        }
        return render(request,'users-add.html',context)
def likes(request):
    try:
       post = get_object_or_404(Post,slug1=request.POST.get('like'))
    except:
        post = get_object_or_404(Post,slug1=request.POST.get('Dislike'))  
    if post.likes.filter(username=request.user).exists():
        post.likes.remove(request.user)
        post.likes_count = post.total_likes()
        post.save()
    else:
        post.likes.add(request.user)
        post.likes_count = post.total_likes()
        post.save()
    
    return redirect('/feed')