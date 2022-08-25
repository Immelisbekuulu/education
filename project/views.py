from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from project.decorators import unauthenticated_user, allowed_users, admin_only
from project.forms import CreateUserForm, SendHomeWorkForm, CommentsForm, DailyMaterialForm, HomeWorkForm, LessonForm, \
    StudyYearForm, GroupForm, StudentForm, StudentGroupForm, AttendenceForm, HomeWorkResultForm, ResultUpdateForm, \
    HomeWorkEvaluationForm
from project.models import StudentGroup, Groups, Lesson, Attendence, Student, HomeWork, Comment, DailyMaterial, \
    StudyYear, HomeWorkResult, HomeWorkEvaluation
from project.sevises import  get_groups, get_home_work, get_groups_id, filter_students_group, \
    get_students_groups_first, filter_groups_lesson, get_lessons_home_work, filter_students_attendence, \
    home_works_result, \
    get_students, study_year, lessons_objects, daily_material_objects, students_attendence, get_studentgroup, \
    get_students_attendence
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect


class StudentsMainView(ListView):
    template_name = "student/students-main-page.html"
    context_object_name = "students"
    model = StudentGroup
    queryset = get_studentgroup()


class GroupsPageView(ListView):
    template_name = "group/groups-page.html"
    context_object_name = "group"
    model = Groups
    queryset = get_groups()


def get_groups_lesson(request, id):
    lesson = Lesson.objects.filter(group=id)
    return render(request, 'lesson/lessons-page.html', {'lesson': lesson})


class AttendencePageView(ListView):
    template_name = "attendence/attendence.html"
    context_object_name = "attendence"
    model = Attendence
    queryset = students_attendence()


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='student')
            user.groups.add(group)

            Student.objects.create(
                user=user,
                name=user.username,
                password=user.password,

            )
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/accounts.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.groups.all()[0].name == 'admin':
                return redirect('prepod')
            elif request.user.groups.all()[0].name == 'student' :
                return redirect('student_page')
            else:
                return HttpResponse('Aut of roles')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['student','admin'])
def userPage(request):
    user = request.user
    student = Student.objects.get(user=user)
    student_groups = StudentGroup.objects.filter(student=student).select_related("group")
    context = {'student': student, 'student_groups': student_groups}
    return render(request, 'student/students-page.html', context)


def students_group(request,id):
    group2 = StudentGroup.objects.select_related("group").filter(id=id).first()
    lesson = Lesson.objects.filter(group=group2.group_id)
    return render(request, 'group/groups-page.html', {'group':group2,'lesson':lesson})


class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lesson/lesson-detail.html'
    context_object_name = "lesson"
    queryset = lessons_objects()
    def get_context_data(self, *args, **kwargs):
        context = super(LessonDetailView,self).get_context_data(*args, **kwargs)
        context["home_work"] = HomeWork.objects.filter(home_work=self.queryset[0])
        return context


def home_work_detail(request,id):
    home_work = HomeWork.objects.get(id=id)
    print(request.POST)
    form = HomeWorkResultForm(request.POST or None)
    if form.is_valid():
        a = form.save(commit=False)
        a.group_id = id
        a.home_work = home_work
        a.save()
        return redirect('student_page')
    return render(request, 'home-work/home-work-detail.html', {'form': form,'title':'Add home work'})


class SendHomeWorkView(CreateView):
    model = HomeWork
    form_class = SendHomeWorkForm
    template_name = "create/send-homework.html"
    success_url = "/"

    def form_valid(self, form: SendHomeWorkForm):
        form.save()
        return redirect("/")

    def form_invalid(self, form: SendHomeWorkForm):
        print("error")
        return redirect("/")


class AddCommentsView(CreateView):
    model = Comment
    form_class = CommentsForm
    template_name = "group/groups-page.html"
    success_url = "/"

    def form_valid(self, form: CommentsForm):
        form.save()
        return redirect("/")

    def form_invalid(self, form: CommentsForm):
        print("error")
        return redirect("/")


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def prepod_cabinet(request):
    group = get_groups()
    student = get_students()
    add_student = get_studentgroup()
    attendence = get_students_attendence()
    date = study_year()
    lesson = lessons_objects()
    dailyMaterial = daily_material_objects()
    homework = get_home_work()
    context = {
        'group':group,
        'student':student,
        'add_student':add_student,
        'attendence':attendence,
        'date':date,
        'lesson':lesson,
        'dailyMaterial':dailyMaterial,
        'homework':homework,
    }
    return render(request,'admin/prepod.html',context)


class CreateGroupView(CreateView):
    model = Groups
    form_class = GroupForm
    template_name = "create/create.html"
    success_url = "prepod"

    def form_valid(self, form: GroupForm):
        form.save()
        return redirect("prepod")

    def form_invalid(self, form: GroupForm):
        print("error")
        return redirect("prepod")

    def get_context_data(self, *args, **kwargs):
        context = super(CreateGroupView, self).get_context_data(*args, **kwargs)
        context["title"] = 'Create Group'
        return context

class CreateStudentView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "create/create.html"
    success_url = "prepod"

    def form_valid(self, form: StudentForm):
        form.save()
        return redirect("prepod")

    def form_invalid(self, form: StudentForm):
        print("error")
        return redirect("prepod")

    def get_context_data(self, *args, **kwargs):
        context = super(CreateStudentView, self).get_context_data(*args, **kwargs)
        context["title"] = 'Create Student'
        return context

def AddStudentView(request,id):
    print(request.POST)
    form = StudentGroupForm(request.POST or None)

    if form.is_valid():
        a = form.save(commit=False)
        a.group_id=id
        a.save()
        return redirect('prepod')
    return render(request, 'create/create.html', {'form': form,'title':'Create Student Group'})

def AttendenceView(request,id):
    print(request.POST)
    form = AttendenceForm(request.POST or None)

    if form.is_valid():
        a=form.save(commit=False)
        a.studentGroup_id=id
        a.save()
        return redirect('prepod')
    return render(request, 'create/create.html', {'form': form,'title':'Check attendence'})

class StudyYearView(CreateView):
    model = StudyYear
    form_class = StudyYearForm
    template_name = "create/create.html"
    success_url = "prepod"

    def form_valid(self, form: StudyYearForm):
        form.save()
        return redirect("prepod")

    def form_invalid(self, form: StudyYearForm):
        print("error")
        return redirect("prepod")

    def get_context_data(self, *args, **kwargs):
        context = super(StudyYearView, self).get_context_data(*args, **kwargs)
        context["title"] = 'Create Study Year'
        return context

def CreateLessonView(request,id):
    print(request.POST)
    form = LessonForm(request.POST or None)

    if form.is_valid():
        a = form.save(commit=False)
        a.group_id=id
        a.save()
        return redirect('prepod')
    return render(request, 'create/create.html', {'form': form,'title':'Check Lesson'})


class CreateMaterialView(CreateView):
    model = DailyMaterial
    form_class = DailyMaterialForm
    template_name = "create/create_materyal.html"
    success_url = "prepod"

    def form_valid(self, form: DailyMaterialForm):
        form.save()
        return redirect("prepod")

    def form_invalid(self, form: DailyMaterialForm):
        print("error")
        return redirect("prepod")


class CreateHomeWorkView(CreateView):
    model = HomeWork
    form_class = HomeWorkForm
    template_name = "create/create_materyal.html"
    success_url = "prepod"

    def form_valid(self, form: HomeWorkForm):
        form.save()
        return redirect("prepod")

    def form_invalid(self, form: HomeWorkForm):
        print("error")
        return redirect("prepod")

    def get_context_data(self, *args, **kwargs):
        context = super(CreateHomeWorkView, self).get_context_data(*args, **kwargs)
        context["title"] = 'Create Home Work'
        return context

class HomeWorkResultView(CreateView):
    model = HomeWorkResult
    form_class = HomeWorkResultForm
    template_name = "home-work/home-work-detail.html"
    success_url = "student_page"

    def form_valid(self, form: HomeWorkResultForm):
        form.save()
        return redirect("student_page")

    def form_invalid(self, form: HomeWorkResultForm):
        print("error")
        return redirect("student_page")

    def get_context_data(self, *args, **kwargs):
        context = super(CreateHomeWorkView, self).get_context_data(*args, **kwargs)
        context["title"] = 'Check Home Works Result'
        return context

class HomeWorkResultUpdate(UpdateView):
    model = HomeWorkResult
    queryset = HomeWorkResult.objects.all()
    form_class = ResultUpdateForm
    template_name = "home-work/home_work_result.html"
    success_url = "prepod"


def detail_group(request, id):
    group = Groups.objects.get(id=id)
    studentGroup1 = StudentGroup.objects.filter(group=id)
    studentGroup2 = StudentGroup.objects.filter(group=id).first()
    lesson1 = Lesson.objects.filter(group=id)
    lesson2 = Lesson.objects.filter(group=id).first()
    home_work = HomeWork.objects.filter(group=id)
    attendence = Attendence.objects.filter(studentGroup=studentGroup2)
    context = {
        'group': group,
        'studentGroup': studentGroup1,
        'lesson': lesson1,
        'home_work': home_work,
        'attendence': attendence,
    }
    return render(request, "create/detail_group.html", context)


def home_work_result(request, id):
    if request.method == "POST":
        form = HomeWorkResultForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.home_work_id = id
            form.save()
            return redirect('prepod')

    form = HomeWorkResultForm()
    return render(request, "home-work/home_work_result.html", {"form": form})

def home_works_result_ball(request):
    result_ball = home_works_result()
    context = {
        'result_ball': result_ball,
    }
    return render(request, "home-work/result_ball.html", context)


def home_works_ball(request, id):
    ball = get_object_or_404(HomeWorkResult, id=id)
    form = HomeWorkResultForm(request.POST or None, instance=ball)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('prepod')
    context = {
        'form': form,
        'ball': ball
    }
    return render(request, "home-work/ball.html", context)


def delete_student(request, id):
    if request.method == "POST":
        Student.objects.get(id=id).delete()
        return redirect('prepod')
    return render(request, "delete/delete.html")

def delete_group(request, id):
    if request.method == "POST":
        Group.objects.get(id=id).delete()
        return redirect('prepod')
    return render(request, "delete/delete.html")

def delete_lesson(request, id):
    if request.method == "POST":
        Lesson.objects.get(id=id).delete()
        return redirect('prepod')
    return render(request, "delete/delete.html")

def delete_home_work(request, id):
    if request.method == "POST":
        HomeWork.objects.get(id=id).delete()
        return redirect('prepod')
    return render(request, "delete/delete.html")

def delete_daily_material(request, id):
    if request.method == "POST":
        DailyMaterial.objects.get(id=id).delete()
        return redirect('prepod')
    return render(request, "delete/delete.html")


class HomeWorkEvaluationView(CreateView):
    model = HomeWorkEvaluation
    form_class = HomeWorkEvaluationForm
    template_name = "create/create.html"
    success_url = "prepod"

    def form_valid(self, form: HomeWorkEvaluationForm):
        form.save()
        return redirect("prepod")

    def form_invalid(self, form: HomeWorkEvaluationForm):
        print("error")
        return redirect("prepod")

    def get_context_data(self, *args, **kwargs):
        context = super(HomeWorkEvaluationView, self).get_context_data(*args, **kwargs)
        context["title"] = 'Add'
        return context


