from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def defaulthomepage(request):
    if request.user.is_authenticated:
        return redirect('login')
    #template = loader.get_template('homepage.html')
    return render(request, 'default_homepage.html')


def studenthomepage(request):
    student = StudentProfile.objects.get(user_id = request.user.id)
    if not request.user.is_authenticated:
        return redirect('defaulthomepage')
    #template = loader.get_template('homepage.html')
    context ={
        'student': student,
    }
    return render(request, 'studenthomepage.html', context)

def teacherhomepage(request):
    if not request.user.is_authenticated:
        return redirect('defaulthomepage')
    teacherobject = Teacher.objects.get(id = request.user.id)
    teacher = TeacherProfile.objects.get(user_id = teacherobject.id)
    context = { "teacher" : teacher}
    #template = loader.get_template('homepage.html')
    return render(request, 'teacherhomepage.html', context)

def scorespage(request, id):
    #scores = Score.objects.all()
    studentmodel = Student.objects.all()
    teacher = TeacherProfile.objects.get(user_id = request.user.id)
    student = StudentProfile.objects.all()
    course = Course.objects.get(pk = id) 
    enrolledstudents = StudentCourseEnrollment.objects.filter(course_id = course)
    chapter = CourseChapter.objects.filter(course_id = course)
    scores = Score.objects.filter(chapter__in = chapter)
    scorescount = scores.count()
    mean_score = 0 
    
    
    if request.user.is_authenticated:
        pass
        for i in scores:
            mean_score  += i.score
        if scorescount == 0:
            mean_score = 0
        else:
            mean_score = mean_score/scorescount
    else:
        return redirect('defaulthomepage')
    context = {
        "mean_score" : mean_score,
        'score' : scores,
        'course': course,
        'student': student,
        'teacher': teacher,
        'studentmodel': studentmodel,
        'enrolledstudent': enrolledstudents,
        'chapter': chapter,
    }
    return render(request, 'scorespage.html', context)


def signupoptions(request):
    if request.user.is_authenticated:
        return redirect('defaulthomepage')
    #template = loader.get_template('homepage.html')
    return render(request, 'signup_options.html')


def studentregister(request):
      if request.user.is_authenticated:
          return redirect('login')
      else:
          form = StudentForm()
          # if this is a POST request we need to process the form data
          if request.method == "POST":
              # create a form instance and populate it with data from the request:
              form = StudentForm(request.POST)
              #form.clean_password2()
              # check whether it's valid:
              if form.is_valid() and form.clean_password2():
                  form.save()
                  # process the data in form.cleaned_data as required
                  user = form.cleaned_data.get('username')
                  # redirect to a new URL:
                  messages.success(request, 'Account was created for ' + user)

                  return redirect('login')
                  # if a GET (or any other method) we'll create a blank form
              #else:
                  #form = UserForm()
          
          context = {"form" : form }
          return render(request, "studentregister.html", context)

def teacherregister(request):
      if request.user.is_authenticated:
          return redirect('login')
      else:
          form = TeacherForm()
          # if this is a POST request we need to process the form data
          if request.method == "POST":
              # create a form instance and populate it with data from the request:
              form = TeacherForm(request.POST)
              #form.clean_password2()
              # check whether it's valid:
              if form.is_valid() and form.clean_password2():
                  form.save()
                  # process the data in form.cleaned_data as required
                  user = form.cleaned_data.get('username')
                  # redirect to a new URL:
                  messages.success(request, 'Account was created for ' + user)

                  return redirect('login')
                  # if a GET (or any other method) we'll create a blank form
              #else:
                  #form = UserForm()
          
          context = {"form" : form }
          return render(request, "teacherregister.html", context)


def coursecreationpage(request):
    if request.user.is_authenticated:
        form = CourseForm()
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            teacherinstance = request.POST['teacherinstance']
            teacherinstanceobject = TeacherProfile.objects.get(pk=teacherinstance)
            #return HttpResponse({'status': 'received form!'})
            if form.is_valid():
                newform = form.save(commit=False)
                newform.teacher = teacherinstanceobject
                form.save()
                messages.success(request,'course created')
                return redirect('yourcourses', teacherinstance)
                
            else: 
                form = CourseForm()
                #return JsonResponse({'status': 'course created!'})
                messages.info(request,'invalid data')
    #if not request.user.is_authenticated:
    else:
        return redirect('defaulthomepage')   
    #template = loader.get_template('homepage.html')
    teacher = TeacherProfile.objects.all()
    context = {'form': form, "teacher": teacher}
    return render(request, 'coursecreationpage.html', context)


def yourcourses(request, id):
    if not request.user.is_authenticated:
        return redirect('defaulthomepage')
    course = Course.objects.filter(teacher_id=id) 
    teacher = TeacherProfile.objects.get(user_id=request.user.id)   
    #template = loader.get_template('homepage.html')
    context = {'course': course, 'teacher': teacher }
    return render(request, 'yourcourses.html', context)

def editcourse(request, id):
    teacher = TeacherProfile.objects.get(user_id=request.user.id)  
    course = Course.objects.get(id=id)  
    if request.user.is_authenticated:
        coursechapterform = CourseChapterForm()
        videoform = ChapterVideoForm()
        if request.method == 'POST':
            #videoform = VideoForm(request.POST, prefix="coursechapterform")
            coursechapterform = CourseChapterForm(request.POST)
            courseinstance = request.POST['course']
            courseinstanceobject = Course.objects.get(pk=courseinstance)
            
            if coursechapterform.is_valid():
                newcoursechapterform = coursechapterform.save(commit=False)
                newcoursechapterform.course = courseinstanceobject
                coursechapterform.save()
                messages.success(request,'chapter created')
                
        
            else: 
                coursechapterform = CourseChapterForm()
                #return JsonResponse({'status': 'course created!'})
                messages.info(request,'invalid data')
    #if not request.user.is_authenticated:
    else:
        return redirect('defaulthomepage') 
    chapter = CourseChapter.objects.filter(course_id=id)
    video = Video.objects.all() 
    context = {'coursechapterform': coursechapterform,
    "videoform":videoform, 
    "course":course,
    "chapter": chapter, 
    "video": video,
    "teacher": teacher}
    return render(request, 'editcourse.html', context)   

def addvideo(request, id):
    if request.user.is_authenticated:
        videoform = ChapterVideoForm()
        if request.method == 'POST':
            videoform = ChapterVideoForm(request.POST, request.FILES )
            #coursechapterform = CourseChapterForm(request.POST)
            #courseinstance = request.POST['course']
            coursechapterinstance = request.POST['coursechapter']
            courseinstance = request.POST['courseid']
            coursechapterobject = CourseChapter.objects.get(pk=coursechapterinstance)
            if videoform.is_valid():
                newvideoform = videoform.save(commit=False)
                #newcoursechapterform = coursechapterform.save(commit=False)
                newvideoform.coursechapter = coursechapterobject
                videoform.save()
                messages.success(request,'video added')
                
    return redirect('editcourse', courseinstance)



def studentdashboard(request):
    if not request.user.is_authenticated:
        return redirect('defaulthomepage')  
    student = StudentProfile.objects.get(user_id = request.user.id)  
    teacherobject = Teacher.objects.all()
    courseenrollment = StudentCourseEnrollment.objects.filter(student_id = student.id)
    coursecount = courseenrollment.count()
    chapter = CourseChapter.objects.all()
    chaptercompleted = ChapterCompleted.objects.all()
    coursescompleted = StudentCourseEnrollment.objects.filter(student_id=student, course_completed=True).count()
    coursespending = StudentCourseEnrollment.objects.filter(student_id=student, course_completed=False).count()
    course = Course.objects.all()
    teacherprofile = TeacherProfile.objects.all()
    score = Score.objects.all()
    context = {
        "course": course,
        "teacherprofile": teacherprofile,
        "teacherobject": teacherobject,
        "student": student, 
        "courseenrollment" : courseenrollment,
        "chapter" : chapter,
        "score" : score,
        "coursecount" : coursecount,
        "chaptercompleted" : chaptercompleted,
        "coursescompleted" : coursescompleted,
         "coursespending" : coursespending


    }
    return render(request, 'studentdashboard.html', context)

def teacherdashboard(request):
    if not request.user.is_authenticated:
        return redirect('defaulthomepage')    
    teacher = TeacherProfile.objects.get(user_id = request.user.id)
    course = Course.objects.filter(teacher_id = teacher)
    coursecount = Course.objects.filter(teacher_id = teacher).count()
    #courseenrolledstudents = StudentCourseEnrollment.objects.filter(course_id = course)
    courseenrolledstudents = StudentCourseEnrollment.objects.all()
    chapter = CourseChapter.objects.all()
    question =Question.objects.all()
    context = {
        "chapter":chapter,
        "teacher": teacher,
        "course":course,
         "coursecount":coursecount,
        "question":question,
        "courseenrolledstudents": courseenrolledstudents
    }
    return render(request, 'teacherdashboard.html', context)


def loginUser(request):
  #template = loader.get_template('homepage.html')
  if request.user.is_authenticated:
    #username = request.POST.get('username')
    #password = request.POST.get('password')
    #user = User.objects.get(pk=user)
    if request.user.role  == "STUDENT":
        return redirect('studenthomepage')
    elif request.user.role == "TEACHER":
        return redirect('teacherhomepage')
  else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                if user.role  == "STUDENT":
                    return redirect('studenthomepage')
                elif user.role == "TEACHER":
                    return redirect('teacherhomepage')
            else:
                messages.info(request,'username OR password is incorrect')

  context = { }
  return render(request, 'login.html', context)

'''def studentchecker(user):
    if user.role is not 'STUDENT' :
        return HttpResponse("You can't visit this page.")


def teacherchecker(user):
    if user.role is 'Student' :
        return HttpResponse("You can't visit this page.")'''

def logoutUser(request):
    logout(request)
    return redirect('login')

    
#@user_passes_test(studentchecker, login_url='/login/')
def studentprofile(request):
    student = StudentProfile.objects.get(user_id = request.user.id)
    if request.method == 'POST':
        u_form = UserChangeForm(request.POST, instance=request.user)
        p_form = StudentProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=student)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('studentprofile')
    else:
        u_form = UserChangeForm(instance=request.user)
        p_form = StudentProfileUpdateForm(instance=student)
 
    
    studentuser = Student.objects.get(id = request.user.id)
    context = {"studentuser" : studentuser,
     "student" : student,
     'u_form': u_form,
        'p_form': p_form }
    return render(request, 'studentprofile.html', context)



#@user_passes_test(teacherchecker, login_url='/login/')
def teacherprofile(request):
    teacher = TeacherProfile.objects.get(user_id = request.user.id)
    if request.method == 'POST':
        u_form = UserChangeForm(request.POST, instance=request.user)
        p_form = TeacherProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=teacher)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('teacherprofile')
    else:
        u_form = UserChangeForm(instance=request.user)
        p_form = TeacherProfileUpdateForm(instance=teacher)
 
    
    teacheruser = Teacher.objects.get(id = request.user.id)
    context = {"teacheruser" : teacheruser,
     "teacher" : teacher,
     'u_form': u_form,
        'p_form': p_form }
    return render(request, 'teacherprofile.html', context)
   


def courses(request):
    course = Course.objects.all()
    student = StudentProfile.objects.get(user_id = request.user.id)
    teacher = TeacherProfile.objects.all()
    enrollment = StudentCourseEnrollment.objects.filter(student_id = student)
    
    context= {"course" : course,
     "enrollment" : enrollment, 
    
      "student" : student,
      "teacher" : teacher
        }
    return render(request, 'courses.html', context)

def studentcourses(request, id):
    course = Course.objects.all()
    teacher = TeacherProfile.objects.all()
    student = StudentProfile.objects.get(user_id = request.user.id)
    enrollment = StudentCourseEnrollment.objects.filter(student_id = student)
    context= {"course" : course,
     "enrollment" : enrollment, 
      "student" : student,
      "teacher" : teacher }
    return render(request, 'studentcourses.html', context)


def fullcoursepage(request, id):
    course = Course.objects.get(pk=id)
    student = StudentProfile.objects.get(user_id = request.user.id)
    coursechapter = CourseChapter.objects.filter(course_id = id)
    video = Video.objects.all()
    chaptercompleted = ChapterCompleted.objects.all()
    enrollment = StudentCourseEnrollment.objects.filter(course_id =course, student_id = student)
    if enrollment.count() == 0:
        enrollment = False
    elif enrollment.count()== 1:
        enrollment = True
    else :
        enrollment = False
    #numberOfEnrolledStudents =  enrollment.count()
    context= {"course" : course,
    "coursechapter" : coursechapter,
     "enrollment" : enrollment, 
     #"numberOfEnrolledStudents" : numberOfEnrolledStudents,
      "student" : student,
      "video" : video,
      "chaptercompleted": chaptercompleted}
    return render(request, 'fullcoursepage.html', context)

def chapterdetails(request, id, course):
    student = StudentProfile.objects.get(user_id = request.user.id)
    chapter = CourseChapter.objects.get(pk=id)
    course = Course.objects.get(pk = course)
    enrollment = StudentCourseEnrollment.objects.filter(course_id =course, student_id = student)
    if enrollment.count() == 0:
        enrollment = False
    elif enrollment.count()== 1:
        enrollment = True
    else :
        enrollment = False
    video = Video.objects.filter(coursechapter = chapter)
    chaptercompleted, created = ChapterCompleted.objects.get_or_create(student = student, chapter = chapter)
    context = {
        "chapter": chapter,
        "video": video,
        "enrollment" : enrollment,
        "status": chaptercompleted,
        "course": course,
        "student": student

    }
    return render(request, 'chapterdetails.html', context)


def deletechapter(request, id, course):
    if request.user.is_authenticated:
        CourseChapter.objects.get(pk=id).delete()
    course = str(course)
    return redirect('editcourse', course)

def deletecourse(request, id):
    if request.user.is_authenticated:
        Course.objects.get(pk=id).delete()
    return redirect('teacherdashboard')

def deletecourse2(request, id, teacher):
    if request.user.is_authenticated:
        Course.objects.get(pk=id).delete()
    return redirect('yourcourses', teacher)



def createquiz(request, id):
    if request.user.is_authenticated:
        questionform = QuestionForm()
        if request.method == 'POST':
            questionform = QuestionForm(request.POST)
            coursechapterinstance = request.POST['chapter']
            coursechapterobject = CourseChapter.objects.get(pk=coursechapterinstance)
            if questionform.is_valid():
                newquestionform = questionform.save(commit=False)
                #newcoursechapterform = coursechapterform.save(commit=False)
                newquestionform.chapter = coursechapterobject
                questionform.save()
                questionform = QuestionForm()
                #messages.success(request,'question added')
    else: 
        return redirect('defaulthomepage')
    chapter = CourseChapter.objects.get(pk = id)
    question = Question.objects.filter(chapter_id = id)
    context={
        "question": question,
        "form" : questionform,
        "chapter" : chapter,
    }
                
    return render(request, 'createquiz.html', context)

def deletequestion(request, id, chapter ):
    if request.user.is_authenticated:
        Question.objects.get(pk=id).delete()
        chapter = str(chapter)
    else:
        return redirect('defaulthomepage')
    return redirect('/createquiz/' + chapter)




def takequiz(request, id, course):
    user = request.user
    student = StudentProfile.objects.get(user_id = request.user.id)
    course = Course.objects.get(pk = course)
    AllChaptersForCourse = CourseChapter.objects.filter(course=course)
    if request.method == 'POST':
        print(request.POST)
        question = Question.objects.filter(chapter_id = id)
        score=0
        wrong=0
        correct=0
        total=0
        for q in question:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        time = request.POST.get('timer')
        if total == 0:
            percent = 0
        else:
            percent = score/(total*10) *100    
        coursechapter = id
        coursechapterobject = CourseChapter.objects.get(pk=id)
        if percent >= 75 & Score.objects.filter(student = student,chapter = coursechapterobject).count() < 1:
            
            Score.objects.create(student = student,chapter = coursechapterobject,score = percent, timeused = time)
            x = ChapterCompleted.objects.get(student = student, chapter = coursechapterobject)
            x.is_completed = True
            x.save()
            y = False
            g = ChapterCompleted.objects.filter(student = student, chapter__in=AllChaptersForCourse)
            for i in g:
                if i.is_completed == False:
                    g = False
            studentcoursecomplete = StudentCourseEnrollment.objects.get(student = student, course=course)
            studentcoursecomplete.course_completed = True
            studentcoursecomplete.save()
        context = {
            'score':score,
            'time': time,
            'course':course,
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total,
            'student': student,
            'coursechapter':coursechapter
        
        }
        return render(request,'quizresults.html',context)
    else:
        question = Question.objects.filter(chapter_id = id)

    question = Question.objects.filter(chapter_id = id)
    context = {
       "question" : question,
       'student': student,
    }
    return render(request, 'takequiz.html', context)



def update_enrolled_courses(request):
    data = json.load(request)
    action = data['action']
    courseId = data['courseId']
    userid = data['userid']
    if action == "add":
        #user = User.objects.get(pk=userid)
        #courseobject = Course.objects.get(pk=courseId)
        #user.profile.enrolled_courses.add(courseobject)
        courseobject = Course.objects.get(pk=courseId)
        userprofileobject = StudentProfile.objects.get(pk=userid)
        #coursename = Course.name.get(pk=courseId)
        check =  StudentCourseEnrollment.objects.filter(course = courseobject, student = userprofileobject ).count()
        if  check == "ObjectDoesNotExist" or check < 1 :
             StudentCourseEnrollment.objects.create(course = courseobject,
             student = userprofileobject ) 
             courseobject.enrolledstudents += 1
             courseobject.save()
             messages.success(request, 'Successfully enrolled for ' + courseobject.name)

        else: 
            messages.warning(request, 'Already enrolled for ' + courseobject.name)
            #messages.info(request, 'Already enrolled for ' )
            #messages.error(request, 'Already enrolled for ')
            return JsonResponse({'status': 'course already enrolled!'})
               
        #courseobject.save()
    elif action == "drop":
        courseobject = Course.objects.get(pk=courseId)
        userprofileobject = StudentProfile.objects.get(pk=userid)
        check =  StudentCourseEnrollment.objects.filter(course = courseobject, student = userprofileobject ).count()
        if  check is not 0 and check >= 1 : 
             StudentCourseEnrollment.objects.get(course = courseobject,
             student = userprofileobject ).delete()
             courseobject.enrolledstudents -= 1
             courseobject.save()
             messages.success(request, 'Successfully dropped ' + courseobject.name)
        else:
            messages.warning(request, 'Already dropped ' + courseobject.name)
    return JsonResponse({'status': 'course enrolled!'})
