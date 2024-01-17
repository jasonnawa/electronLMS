from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField


#class UserForm(ModelForm):
#    class Meta:
#        model = User
#        fields = ['username', 'first_name','last_name','email', 'password','role']


'''class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'first_name','last_name','email', 'password']'''

#class TeacherForm(ModelForm):
 #   class Meta:
  #      model = Teacher
   #     fields = ['username', 'first_name','last_name','email', 'password']


class StudentForm(ModelForm):#forms.MOdelForm
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Student
        fields = ["first_name","last_name","username","email", "password1", "password2"]

        widgets = {
            "first_name" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter firstname'}),
            "last_name" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter lastname'}),   
            "username" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter username'}),
            "email" :forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Enter E-mail'}),
            "password1" :forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Enter password'}),
            "passwor2" :forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirm password'}),
            
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class TeacherForm(ModelForm):#forms.MOdelForm
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Teacher
        fields = ["first_name","last_name","username","email", "password1", "password2"]

        widgets = {
            "first_name" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter firstname'}),
            "last_name" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter lastname'}),   
            "username" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter username'}),
            "email" :forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Enter E-mail'}),
            "password1" :forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Enter password'}),
            "passwor2" :forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirm password'}),
            
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['image', 'phone', 'mobile' , 'address']

        widgets = {
            "image" :forms.FileInput(attrs={'class':'form-control'}),
            "address" :forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Enter Address'}),   
            "phone" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter phone'}),
            "mobile" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Mobile'}),
            
        }
class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['image', 'phone', 'mobile' , 'address']
        
        
        widgets = {
            "image" :forms.FileInput(attrs={'class':'form-control'}),
            "address" :forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Enter Address'}),   
            "phone" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter phone'}),
            "mobile" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Mobile'}),
            
        }

class CourseForm(forms.ModelForm):
     """A form for creating new courses. Includes all the required
     fields"""

     class Meta:
        model = Course
        fields = ["teacher","name", "description", "displayimage"]

        widgets = {
            "name" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter course Name'}),
            "description" :forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Enter course description'}),
             "displayimage" :forms.FileInput(attrs={'class':'form-control'}),
            
        }

class CourseChapterForm(ModelForm):

     class Meta:
        model = CourseChapter
        fields = ["course", "topic", "introduction", "body"]

        widgets = {
            "topic" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter chapter topic'}),
            "introduction" :forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Enter chapter introduction'}),
             "body" :forms.Textarea(attrs={'class':'form-control',  'placeholder': 'Enter chapter body'}),
            
        }

class ChapterVideoForm(ModelForm):

     class Meta:
        model = Video
        fields = ["coursechapter", "name", "videofile"]
        
        widgets = {
            "name" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter video Name'}),
             "videofile" :forms.FileInput(attrs={'class':'form-control'}),
            
        }



class QuestionForm(ModelForm):
    class Meta:
        model=Question
        fields= ["chapter", "question", "op1", "op2", "op3", "op4", "ans"]

        widgets = {
            "question" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter question'}),
             "op1" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter option 1'}),
             "op2" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter option 2'}),
             "op3" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter option 3'}),
             "op4" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter option 4'}),
             "ans" :forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter correct answer'}),
            
        }