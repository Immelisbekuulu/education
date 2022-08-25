from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from project.models import HomeWork, Lesson, Comment
from project.sevises import students_password


class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username...'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email...'}))
    password1 = forms.IntegerField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password...'}))
    password2 = forms.IntegerField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password...'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SendHomeWorkForm(forms.ModelForm):
    home_work = forms.ModelChoiceField(queryset=Lesson.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = HomeWork
        fields = ('__all__')


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('__all__')


from django import forms
from .models import *


class GroupForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ('__all__')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('__all__')


class StudentGroupForm(forms.ModelForm):
    class Meta:
        model = StudentGroup
        fields = ('student',)


class AttendenceForm(forms.ModelForm):
    class Meta:
        model = Attendence
        fields = ('check_student',)


class StudyYearForm(forms.ModelForm):
    class Meta:
        model = StudyYear
        fields = ('__all__')


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('daily_material',)


class DailyMaterialForm(forms.ModelForm):
    class Meta:
        model = DailyMaterial
        fields = ('__all__')


class HomeWorkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        fields = ('__all__')


class HomeWorkResultForm(forms.ModelForm):
    class Meta:
        model = HomeWorkResult
        fields = ('student', 'print_home_work',)


class ResultUpdateForm(forms.ModelForm):
    class Meta:
        model = HomeWorkResult
        fields = '__all__'


class HomeWorkEvaluationForm(forms.ModelForm):
    class Meta:
        model = HomeWorkEvaluation
        fields = '__all__'