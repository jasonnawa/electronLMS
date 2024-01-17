from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from django import forms
from .forms import *
# Register your models here

'''class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        #("Personal info", {"fields": ["date_of_birth"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []'''

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(User)
#admin.site.register(Category)
admin.site.register(Course)
admin.site.register(StudentCourseEnrollment)
admin.site.register(CourseChapter)
admin.site.register(Video)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Score)
admin.site.register(ChapterCompleted)
#admin.site.unregister(Group)