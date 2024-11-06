from django.urls import path,include,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.home,name='home'),
    path('test',views.test,name='test'),
    path('loginpage',views.loginpage,name='loginpage'),
    path('teachersignup',views.teachersignup,name='teachersignup'),
    path('studentsignup',views.studentsignup,name='studentsignup'),
    path('contact',views.contact,name='contact'),
    path('adminmenu',views.adminmenu,name='adminmenu'),
    path('addcourse',views.addcourse,name='addcourse'),
    path('addtocourse',views.addtocourse,name='addtocourse'),
    path('sreg',views.sreg,name='sreg'),
    path('treg',views.treg,name='treg'),
    path('approvel',views.approvel,name='approvel'),
    path('approved/<int:id>',views.approved,name='approved'),
    path('disapproved/<int:id>',views.disapproved,name='disapproved'),
    path('coursemanage',views.coursemanage,name='coursemanage'),
    path('showstud',views.showstud,name='showstud'),
    path('showteach',views.showteach,name='showteach'),
    path('showteachatd',views.showteachatd,name='showteachatd'),
   
    path('attendancesearch', views.attendance_search_view, name='attendance_search_view'),
    path('attendancedetails', views.attendance_details_view, name='attendance_details_view'),
    path('submit_attendance_view',views.submit_attendance_view,name='submit_attendance_view'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('loginp',views.loginp,name='loginp'),
    path('delete_student/<int:id>',views.delete_student,name='delete_student'),
    path('delete_teach/<int:id>',views.delete_teach,name='delete_teach'),
    path('assign_teacher/<int:student_id>/<int:teacher_id>/',views.assign_teacher,name='assign_teacher'),
    path('assign',views.assign,name='assign'),
    path('teachermenu',views.teachermenu,name='teachermenu'),
    path('studentmenu',views.studentmenu,name='studentmenu'),
    path('resetpas',views.resetpas,name='resetpas'),
    path('resetpas1',views.resetpas1,name='resetpas1'),
    path('viewstud',views.viewstud,name='viewstud'),
    path('delete_student1/<int:id>',views.delete_student1,name='delete_student1'),

    path('submit_attendance_stud',views.submit_attendance_stud,name='submit_attendance_stud'),
    path('markstudatnd',views.markstudatnd,name='markstudatnd'),
    path('attendancedetailsstud', views.attendance_details_stud, name='attendance_details_stud'),
    path('attendancesearchstud', views.attendance_search_stud, name='attendance_search_stud'),
    path('coursemanaget',views.coursemanaget,name='coursemanaget'),
    path('sresetpas',views.sresetpas,name='sresetpas'),
    path('resetpas2',views.resetpas2,name='resetpas2'),

    path('attendance_stud',views.attendance_stud,name='attendance_stud'),
    path('stdattendance_details_view',views.stdattendance_details_view,name='stdattendance_details_view'),
    path('coursemanages',views.coursemanages,name='coursemanages'),
    path('stdownatend',views.stdownatend,name='stdownatend'),
    path('stdprofile',views.stdprofile,name='stdprofile'),
    path('seditp',views.seditp,name='seditp'),
    path('sedit',views.sedit,name='sedit'),
    path('teownatendser',views.teownatendser,name='teownatendser'),
    path('teownatendserp',views.teownatendserp,name='teownatendserp'),
    path('stdownatendser',views.stdownatendser,name='stdownatendser'),
    path('teassigntask',views.teassigntask,name='teassigntask'),
    path('teassigntask_view',views.teassigntask_view,name='teassigntask_view'),
    path('teviewtask',views.teviewtask,name='teviewtask'),
    path('student/tasks/', views.student_task_list, name='student_task_list'),  # URL for student task list
    path('student/tasks/<int:task_id>/submit/', views.stask_create, name='stask_create'),  # URL for submission    path('teacher/submissions/', views.teacher_view_submissions, name='teacher_view_submissions'),
    path('teacher/submissions/', views.teacher_view_submissions, name='teacher_view_submissions'),


]
