from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now




class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'admin'
        STUDENT = "STUDENT", 'Student'
        TEACHER = "TEACHER", 'Teacher'
    
    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            self.role = self.role
            return super().save(*args, **kwargs)

class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role = User.Role.STUDENT)

class Student(User):

    base_role = User.Role.STUDENT
     
    student = StudentManager()
    class Meta:
        proxy = True

    def welcome(self):
        return "ONly for studentrs"

@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STUDENT":
        StudentProfile.objects.create(user=instance)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='team-1.jpg', upload_to='profile_pics')
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20,blank=True)
    address = models.TextField(blank=True)

    def __str__(self): 
         return self.user.username
    

class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role = User.Role.TEACHER)

class Teacher(User):

    base_role = User.Role.TEACHER
    teacher = TeacherManager()
    class Meta:
        proxy = True

    def welcome(self):
        return "ONly for teachers"

@receiver(post_save, sender=Teacher)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "TEACHER":
        TeacherProfile.objects.create(user=instance)
    

class TeacherProfile(models.Model):
    user = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    image = models.ImageField(default='team-1.jpg', upload_to='profile_pics')
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20,blank=True)
    address = models.TextField(blank=True)

    def __str__(self): 
         return self.user.username

class Course(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    displayimage = models.ImageField(upload_to='images', default="defaultcourseimage.jpg")
    enrolledstudents = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=now, blank=True)
    
    def __str__(self): 
         return self.name   
    #@property
    #def addstudent(self):
    #    enrolledstudents = self.enrolledstudents + 1
     #   return enrolledstudents

class StudentCourseEnrollment(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
  enrolled_time = models.DateTimeField(default=now, blank=True)
  course_completed = models.BooleanField(default=False, null=False)

  def __str__(self): 
         return (f'{self.student} "enrolled in course " {self.course}')

#class EnrollmentManager(models.Manager):
   # def create_instance(self, course, student):
    #    enrolled = self.create(title= title)
        # do something with the book
     #   return book

class CourseChapter(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  topic = models.CharField(max_length=55, null=False)
  introduction = models.TextField(null=True, default="coursechapterintro")
  body = models.TextField(null = True, default="CourseChapterbody")
  upload_time = models.DateTimeField(auto_now_add=True)

  def __str__(self): 
         return self.topic

class Video(models.Model):
    coursechapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE)
    name = models.CharField(max_length = 60)
    videofile = models.FileField(upload_to='videos/', null=True)
    
    def __str__(self):

        return self.name

class Question(models.Model):
    chapter =  models.ForeignKey(CourseChapter, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.question

class Quiz(models.Model):
    coursechapter= models.ForeignKey(CourseChapter, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)


class Score(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE)
    score = models.IntegerField(null=False, default=0)
    timeused = models.IntegerField(null=True)

class ChapterCompleted(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False, null=False)

#class CourseCompleted(models.Model):
 #   student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
  #  course = models.ForeignKey(Course, on_delete=models.CASCADE)
   # is_completed = models.BooleanField(default=False, null=False)

