from django.shortcuts import render,redirect,get_object_or_404
from tution.models import Course,Student,Teacher,CustomUser,Attendance,Stdattendance,Task,Stask
from django.contrib import messages,auth
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
import random
import re
import os


def test(request):
    return render(request,'test.html')

def home(request):
    return render(request,'home.html')

def loginpage(request):
    return render(request,'login.html')

def teachersignup(request):
    course=Course.objects.all()
    return render(request,'teachersignup.html',{'course':course})

def studentsignup(request):
    course=Course.objects.all()
    return render(request,'studentsignup.html',{'course':course})

def contact(request):
    return render(request,'contact.html')

@login_required(login_url='loginpage')
def adminmenu(request):
    count = CustomUser.objects.filter(status='0').filter(~Q(user_type='1')).count()
    return render(request,'adminmenu.html',{'count':count,'active_page': 'adminmenu'})

@login_required(login_url='loginpage')
def addcourse(request):
    count = CustomUser.objects.filter(status='0').filter(~Q(user_type='1')).count()
    return render(request,'addcourse.html', {'active_page': 'addcourse','count':count})

@login_required(login_url='loginpage')
def showstud(request):
    count = CustomUser.objects.filter(status='0').filter(~Q(user_type='1')).count()
    student=Student.objects.filter(user__status='1')
    return render(request,'showstud.html',{'student':student,'count':count,'active_page': 'showstud'})

@login_required(login_url='loginpage')
def showteach(request):
    count = CustomUser.objects.filter(status='0').filter(~Q(user_type='1')).count()
    teacher=Teacher.objects.filter(user__status='1')
    return render(request,'showteach.html',{'teacher':teacher,'count':count,'active_page': 'showteach'})

@login_required(login_url='loginpage')
def showteachatd(request):
    count = CustomUser.objects.filter(status='0').filter(~Q(user_type='1')).count()
    teacher=Teacher.objects.filter(user__status='1')
    return render(request,'tattendance.html',{'teacher':teacher,'count':count,'active_page': 'showteachatd'})

@login_required(login_url='loginpage')
def attendance_search_view(request):
    count = CustomUser.objects.filter(status='0').filter(~Q(user_type='1')).count()
    teacher=Teacher.objects.filter(user__status='1')
    return render(request, 'tattendview.html', {'teacher': teacher,'count':count,'active_page': 'attendance_search_view'})

#login
def loginp(request):
    if request.method=='POST':
        username=request.POST.get('uname')
        password=request.POST.get('pswd')
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.user_type == '1':
               auth.login(request,user)
               return redirect('adminmenu')
            elif user.user_type == '3':
               auth.login(request,user)
               return redirect('studentmenu')
            else:
                auth.login(request,user)
                return redirect('teachermenu')
        else:
            messages.error(request,'Incorrect username or Password')
            return redirect('loginpage')
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('loginpage')




@login_required(login_url='loginpage')
def attendance_details_view(request):
    teacher= None
    attendance_records=[]
    start_date=end_date=None
    if request.method=='POST':
        teacher_id = request.POST.get('teacherName')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        
        teacher = get_object_or_404(Teacher,id=teacher_id)
        attendance_records = Attendance.objects.filter(
            teacher=teacher,
            date__range=[start_date, end_date]
        )
        return render(request, 'tattendshow.html',{'teacher':teacher,'attendance': attendance_records,
                'start_date': start_date,
                'end_date': end_date,'active_page': 'attendance_search_view'})

@login_required(login_url='loginpage')
def submit_attendance_view(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        date = request.POST.get('adate')
        status = request.POST.get('status')

        if teacher_id and date and status:
            teacher = Teacher.objects.get(id=teacher_id)
            Attendance.objects.create(
                teacher=teacher,
                date=date,
                status=status
            )
            messages.success(request, 'Attendance submitted successfully!')
            return redirect('showteachatd')

    teachers = Teacher.objects.all()
    return render(request, 'tattendance.html', {'teachers': teachers})        

#admin
@login_required(login_url='loginpage')    
def assign(request):
    count = CustomUser.objects.filter(status='0').filter(~Q(user_type='1')).count()
    course=Course.objects.all()
    student=Student.objects.filter(user__status='1')
    teacher=Teacher.objects.filter(user__status='1')
    return render(request,'assignteacher.html',{'count':count,'active_page': 'assign','teacher':teacher,'student':student,'course':course})

def assign_teacher(request,student_id,teacher_id):
    student=CustomUser.objects.get(id=student_id)
    teacher=CustomUser.objects.get(id=teacher_id)
    user=Student.objects.get(user=student)
    user.teacher=teacher
    user.save()
    return redirect('assign')
    
def addtocourse(request):
    if request.method=="POST":
        course_name=request.POST['cource']
        Fees=request.POST['fee']
        duration=request.POST['duration']
        syllabus=request.FILES.get('file')
        cor=Course(course_name=course_name,Fees=Fees,duration=duration,syllabus=syllabus)
        cor.save()
        messages.success(request,'course added')
        return redirect('addcourse')
    
@login_required(login_url='loginpage')    
def coursemanage(request):
    count = CustomUser.objects.filter(status='0').filter(~Q(user_type='1')).count()
    cor=Course.objects.all()
    return render(request,'coursemanage.html',{'cor':cor,'count':count,'active_page': 'coursemanage'})

@login_required(login_url='loginpage')    
def approvel(request):
    count = CustomUser.objects.filter(status='0').filter(~Q(user_type='1')).count()
    users=CustomUser.objects.filter(~Q(user_type='1'))
    for user in users:
        if user.user_type == '2':
            user.details=Teacher.objects.filter(user=user).first()
        if user.user_type == '3':
            user.details=Student.objects.filter(user=user).first()
    return render(request,'approvel.html',{'users':users,'count':count,'active_page': 'approvel'})

def approved(request,id):
    usr=CustomUser.objects.get(id=id)
    if usr.user_type == '2' or usr.user_type == '3':
        usr.status = '1'
        usr.save()
        pasw=CustomUser.objects.get(id=id)
        if usr.user_type == '2':
            ut=Teacher.objects.get(user=id)
        if usr.user_type == '3':
            ut=Student.objects.get(user=id)
        pas=str(random.randint(100000,999999))
        pasw.set_password(pas)
        pasw.save()
        uname=ut.user.username
        umail=ut.user.email
        subject='Admin Approved'
        message='username:'+str(uname)+"\n"+'password:'+str(pas)+"\n"+'email:'+str(umail)
        send_mail(subject,message,settings.EMAIL_HOST_USER,{usr.email})
        messages.info(request,'User Approved')
        return redirect('approvel')

def disapproved(request,id):
    usr=CustomUser.objects.get(id=id)
    if usr.user_type == '2' or usr.user_type == '3':
        usr.status = '1'
        usr.save()
        if usr.user_type == '2':
            ut=Teacher.objects.get(user=id)
            ut.delete()
            ut.user.delete()
        if usr.user_type == '3':
            ut=Student.objects.get(user=id)
            ut.delete()
            ut.user.delete()
        subject='Admin Dispproved'
        message='Sorry,Your request disapproved.'
        send_mail(subject,message,settings.EMAIL_HOST_USER,{usr.email})
        messages.warning(request,'User dispproved')
        return redirect('approvel')

def delete_student(request,id):
    reg=Student.objects.get(id=id)
    reg.delete()
    reg.user.delete()
    return redirect('showstud')

def delete_teach(request,id):
    reg=Teacher.objects.get(id=id)
    reg.delete()
    reg.user.delete()
    return redirect('showteach')

@login_required(login_url='loginpage')
def stdattendance_details_view(request):
    student= None
    attendance_records=[]
    start_date=end_date=None
    if request.method=='POST':
        student_id = request.POST.get('studentName')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        
        student = get_object_or_404(Student,id=student_id)
        attendance_records = Stdattendance.objects.filter(
            student=student,
            date__range=[start_date, end_date]
        )
        return render(request, 'admstdatend.html',{'student':student,'attendance': attendance_records,
                'start_date': start_date,
                'end_date': end_date,'active_page': 'stdatend'})

def attendance_stud(request):
    student=Student.objects.filter(user__status='1')
    return render(request, 'admstdatendse.html', {'student': student,'active_page': 'stdatend'})
   
#user
    
def treg(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['usrname']
        email=request.POST['mail']
        age=request.POST['age']
        phone_number=request.POST['phone_number']
        sel=request.POST['sel']
        cource1=Course.objects.get(id=sel)
        image=request.FILES.get('image')
        user_type=request.POST['tp']

        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username exist') 
            return redirect('teachersignup')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email exist') 
            return redirect('teachersignup')
        
        if not (phone_number.isdigit and len(phone_number) ==10):
            messages.warning(request,'Phone number must be 10 digits') 
            return redirect('teachersignup')

        if email and not re.match(regex,email):
            messages.warning(request,'Invalid Email')
            return redirect('teachersignup')
           
        else:
            user=CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                user_type=user_type
                )
            user.save()
            teach=Teacher(user=user,age=age,phone_number=phone_number,course=cource1,image=image)
            teach.save()
            messages.success(request,'Registration succesfull.Please wait for admin approval')

        return redirect('teachersignup')
    return render(request,'login.html')

def sreg(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['usrname']
        email=request.POST['mail']
        age=request.POST['age']
        phone_number=request.POST['phone_number']
        sel=request.POST['sel']
        cource1=Course.objects.get(id=sel)
        image=request.FILES.get('image')
        user_type=request.POST['tp']

        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username exist') 
            return redirect('studentsignup')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email exist') 
            return redirect('studentsignup')
        
        if not (phone_number.isdigit and len(phone_number) ==10):
            messages.warning(request,'Phone number must be 10 digits') 
            return redirect('studentsignup')
        
        if email and not re.match(regex,email):
            messages.warning(request,'Invalid Email')
            return redirect('studentsignup')
            
        else:
            user=CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                user_type=user_type
                )
            user.save()
            teach=Student(user=user,age=age,phone_number=phone_number,course=cource1,image=image)
            teach.save()
            messages.success(request,'Registration succesfull.Please wait for admin approval')
        return redirect('studentsignup')
    return render(request,'login.html')



#student
def studentmenu(request):
    student = get_object_or_404(Student,user=request.user)
    return render(request,'astudentmenu.html',{'student':student,'active_page': 'studentmenu'})

@login_required(login_url='loginpage')    
def coursemanages(request):
    cor=get_object_or_404(Student,user=request.user)
    return render(request,'stdcourse.html',{'cor':cor,'active_page': 'coursemanages'})

def stdownatend(request):
    student = get_object_or_404(Student,user=request.user)
    cor=Stdattendance.objects.filter(student=student)
    return render(request,'stdownatendser.html',{'cor':cor,'active_page': 'atnds'})

@login_required(login_url='loginpage')
def stdownatendser(request):
    attendance_records=[]
    start_date=end_date=None
    if request.method=='POST':
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        
        student = get_object_or_404(Student,user=request.user)
        attendance_records = Stdattendance.objects.filter(
            student=student,
            date__range=[start_date, end_date]
        )
        return render(request, 'stdownatend.html',{'student':student,'attendance': attendance_records,
                'start_date': start_date,
                'end_date': end_date,'active_page': 'atnds'})


def stdprofile(request):
    student = get_object_or_404(Student,user=request.user)
    return render(request,'studentprofile.html',{'student':student,'active_page': 'pro'})

def seditp(request):
    student = get_object_or_404(Student,user=request.user)
    course=Course.objects.all()
    return render(request,'studentproedit.html',{'student':student,'course':course,'active_page': 'pro'})


def sedit(request):
    user=request.user
    if request.method=='POST':
        student=get_object_or_404(Student,user=user)
        usr=CustomUser.objects.get(id=user.id)
        usr.first_name=request.POST.get('first_name')
        usr.last_name=request.POST.get('last_name')
        usr.username=request.POST.get('usrname')
        usr.email=request.POST.get('mail')
        student.age=request.POST.get('age')
        student.phone_number=request.POST.get('phone_number')
        sel=request.POST.get('sel')
        course_id=Course.objects.get(id=sel)
        student.course=course_id
        if len(request.FILES)!=0:
            if len(student.image)>0:
                os.remove(student.image.path)
            student.image = request.FILES.get('image')
        usr.save()
        student.save()
        messages.success(request,'Profile Updated')
        return redirect('stdprofile')
    


def sresetpas(request):
    return render(request,'srestpas.html',{'active_page': 'sresetpas'})
def resetpas2(request):
    if request.method=='POST':
        pas=request.POST['pswd']
        pas1=request.POST['pswd1']
        pas2=request.POST['pswd2']
        if request.user.check_password(pas):
            if pas1==pas2:
                if len(pas1)< 6 or not any(char.isupper() for char in pas1) or not any(char.isdigit() for char in pas1) or not any(char in '!@#$%^&(){[}].;<>|?/`~' for char in pas1):
                    messages.error(request,'Password must be at least minimum 6 charecters and contain uppercase and special charecters and digits')
                    return redirect('sresetpas')
                else:
                    request.user.set_password(pas1)
                    request.user.save()
                    update_session_auth_hash(request,request.user)
                    messages.success(request,'Password reset Succesfully')
                    return redirect('sresetpas')
            else:
                messages.error(request,'Passwords Does not match')
                return redirect('sresetpas')
        else:
            messages.error(request,'Incorrect Password')
            return redirect('sresetpas')
               
 
#teacher
def teachermenu(request):
    teacher = get_object_or_404(Teacher,user=request.user)
    return render(request,'ateachermenu.html',{'teacher':teacher,'active_page': 'teachermenu'})

def resetpas(request):
    return render(request,'teresetpas.html',{'active_page': 'resetpas'})

def resetpas1(request):
    if request.method=='POST':
        pas=request.POST['pswd']
        pas1=request.POST['pswd1']
        pas2=request.POST['pswd2']
        if request.user.check_password(pas):
            if pas1==pas2:
                if len(pas1)< 6 or not any(char.isupper() for char in pas1) or not any(char.isdigit() for char in pas1) or not any(char in '!@#$%^&(){[}].;<>|?/`~' for char in pas1):
                    messages.error(request,'Password must be at least minimum 6 charecters and contain uppercase and special charecters and digits')
                    return redirect('resetpas')
                else:
                    request.user.set_password(pas1)
                    request.user.save()
                    update_session_auth_hash(request,request.user)
                    messages.success(request,'Password reset Succesfully')
                    return redirect('resetpas')
            else:
                messages.error(request,'Passwords Does not match')
                return redirect('resetpas')
        else:
            messages.error(request,'Incorrect Password')
            return redirect('resetpas')
               
 
@login_required(login_url='loginpage')
def viewstud(request):
    student=Student.objects.filter(user__status='1').filter(teacher=request.user)
    return render(request,'teviewstudent.html',{'student':student,'active_page': 'viewstud'})
       
def delete_student1(request,id):
    reg=Student.objects.get(id=id)
    reg.delete()
    reg.user.delete()
    return redirect('viewstud')

def markstudatnd(request):
    student=Student.objects.filter(user__status='1').filter(teacher=request.user)
    return render(request,'testudattendmark.html',{'student':student,'active_page': 'mark'})

@login_required(login_url='loginpage')
def submit_attendance_stud(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        date = request.POST.get('adate')
        status = request.POST.get('status')

        if student_id and date and status:
            student = Student.objects.get(id=student_id)
            Stdattendance.objects.create(
                student=student,
                date=date,
                status=status
            )
            messages.success(request, 'Attendance submitted successfully!')
            return redirect('markstudatnd')

    student = Student.objects.all()
    return render(request, 'testudattendmark.html', {'student': student})        

@login_required(login_url='loginpage')
def attendance_details_stud(request):
    student= None
    attendance_records=[]
    start_date=end_date=None
    if request.method=='POST':
        student_id = request.POST.get('studentName')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        
        student = get_object_or_404(Student,id=student_id)
        attendance_records = Stdattendance.objects.filter(
            student=student,
            date__range=[start_date, end_date]
        )
        return render(request, 'testudatv.html',{'student':student,'attendance': attendance_records,
                'start_date': start_date,
                'end_date': end_date,})

@login_required(login_url='loginpage')
def attendance_search_stud(request):
    student=Student.objects.filter(user__status='1').filter(teacher=request.user)
    return render(request, 'testudats.html', {'student': student,'active_page': 'attendance_search_stud'})

@login_required(login_url='loginpage')    
def coursemanaget(request):
    cor=get_object_or_404(Teacher,user=request.user)
    return render(request,'tecourseshow.html',{'cor':cor,'active_page': 'coursemanaget'})


@login_required(login_url='loginpage')    
def teownatendserp(request):
    teacher = get_object_or_404(Teacher,user=request.user)
    cor=Attendance.objects.filter(teacher=teacher)
    return render(request,'teownatendser.html',{'teacher':teacher,'cor':cor,'active_page': 'atnd'})


@login_required(login_url='loginpage')
def teownatendser(request):
    attendance_records=[]
    start_date=end_date=None
    if request.method=='POST':
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        
        teacher = get_object_or_404(Teacher,user=request.user)
        attendance_records = Attendance.objects.filter(
            teacher=teacher,
            date__range=[start_date, end_date]
        )
        return render(request, 'teownatend.html',{'teacher':teacher,'attendance': attendance_records,
                'start_date': start_date,
                'end_date': end_date,'active_page': 'atnd'})


#assignment
#teacher
def teassigntask(request):
    return render(request,'teassigntask.html',{'active_page':'teassigntask'})

def teassigntask_view(request):
    if request.method == 'POST':
        taskname = request.POST.get('task')
        startdate = request.POST.get('startDate')
        enddate = request.POST.get('endDate')

        Task.objects.create(
                taskname=taskname,
                startdate=startdate,
                enddate=enddate,
                teacher=request.user
            )
        messages.success(request, 'Task assigned successfully!')
        return redirect('teassigntask')

    return render(request, 'teassigntask.html')        

def teviewtask(request):
    task=Task.objects.filter(teacher=request.user)
    return render(request,'tetaskview.html',{'task':task,'active_page':'taskv'})
def teacher_view_submissions(request):
    teacher = request.user

    submissions = Stask.objects.filter(student__teacher=teacher).select_related('student', 'task')

    return render(request, 'teacher_view_submissions.html', {'submissions': submissions})



#student


def student_task_list(request):
    student=Student.objects.get(user=request.user)
    teacher=student.teacher
    tasks = Task.objects.filter(teacher=teacher)
    submitted_task_ids = Stask.objects.filter(student=student).values_list('task_id', flat=True)    
    return render(request, 'stdtaskview.html', {'tasks': tasks,'active_page':'taskstd','submitted_task_ids': submitted_task_ids})

def stask_create(request, task_id):
    
    task = get_object_or_404(Task, id=task_id)
    student=Student.objects.get(user=request.user)

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        description = request.POST.get('description')

        if uploaded_file and description:
            stask = Stask(
                task=task,
                student=student,
                pdf=uploaded_file,
                description=description
            )
            stask.save()
            messages.success(request,'Task submitted')
            return redirect('student_task_list') 

    return render(request, 'stdsubmittask.html', {'task': task,'active_page':'taskstd'})

