
from django.urls import path, include
from LMSapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #anyone
    path('', views.defaulthomepage, name="defaulthomepage"),
    path('signupoptions/', views.signupoptions, name="signupoptions"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    #students
    path('studenthome/', views.studenthomepage, name="studenthomepage"),
    path('signupoptions/studentregister/', views.studentregister, name="studentregister"),
    path('studentprofile/', views.studentprofile, name="studentprofile"),
    path('home/courses/', views.courses, name="courses"),
     path('home/studentcourses/<int:id>/', views.studentcourses, name="studentcourses"),
    path('update_enrolled_courses/', views.update_enrolled_courses, name="update_enroll"),
    path('fullcourse/<int:id>/', views.fullcoursepage, name="fullcoursepage"),
    path('chapterdetails/<int:id>/<int:course>/', views.chapterdetails, name="chapterdetails"),
    path('studentdashboard/', views.studentdashboard, name="studentdashboard"),
    path('takequiz/<int:id>/<int:course>/', views.takequiz, name="takequiz"),
    #path('quizresult/', views.quizresult, name="quizresult"),

    #teachers
    path('teacherhome/', views.teacherhomepage, name="teacherhomepage"),
    path('signupoptions/teacherregister/', views.teacherregister, name="teacherregister"),
    path('teacherprofile/', views.teacherprofile, name="teacherprofile"),
    path('yourcourses/<int:id>/', views.yourcourses, name="yourcourses"),
    path('addvideo/<int:id>/', views.addvideo, name="addvideo"),
    path('editcourse/<int:id>/', views.editcourse, name="editcourse"),
    path('teacherhome/yourcourses/createcourse', views.coursecreationpage, name="coursecreationpage"),
    path('teacherdashboard/', views.teacherdashboard, name="teacherdashboard"),
    path('createquiz/<int:id>', views.createquiz, name="createquiz"),
    path('deletequestion/<int:id>/<int:chapter>/', views.deletequestion, name="deletequestion"),
    path('deletechapter/<int:id>/<int:course>/', views.deletechapter, name="deletechapter"),
    path('deletecourse/<int:id>/', views.deletecourse, name="deletecourse"),
    path('deletecourse/<int:id>/<int:teacher>/', views.deletecourse2, name="deletecourse2"),
    path('scorespage/<int:id>/', views.scorespage, name="scorespage"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)