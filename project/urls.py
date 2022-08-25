
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import LessonDetailView, HomeWorkEvaluation, HomeWorkEvaluationView

urlpatterns = [
    path('students_page/', views.StudentsMainView.as_view(), name='students_main_page'),
    path('students_group', views.GroupsPageView.as_view(), name='students_group'),

    path('groups_lesson/<int:id>/', views.get_groups_lesson, name='groups_lesson'),
    path('studentgroup/<int:id>/', views.students_group, name='studentgroup'),

    path('student', views.userPage, name="student_page"),

    path('accounts/', views.registerPage, name="accounts"),
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('send_home_work', views.SendHomeWorkView.as_view(), name='send_home_work'),

    path('prepod/', views.prepod_cabinet, name='prepod'),
    path('create_groupe/', views.CreateGroupView.as_view(), name='create_groupe'),
    path('create_student/', views.CreateStudentView.as_view(), name='create_student'),
    path('add_student/<id>', views.AddStudentView, name='add_student'),
    path('attendance_student/<id>', views.AttendenceView, name='attendance_student'),
    path('studyYear/', views.StudyYearView.as_view(), name='studyYear'),
    path('create_lesson/<id>', views.CreateLessonView, name='create_lesson'),
    path('create_materyal/', views.CreateMaterialView.as_view(), name='create_materyal'),
    path('create_homework/', views.CreateHomeWorkView.as_view(), name='create_homework'),
    path('homework/result/', views.HomeWorkResultView.as_view(), name='homework_result'),
    path('homework/result/<int:pk>/update/', views.HomeWorkResultUpdate.as_view(), name='homework_result_update'),
    path('detail_group/<id>', views.detail_group, name='detail_group'),
    path('home_work_result/<id>',views.home_work_result,name='home_work_result'),
    path('result_ball/',views.home_works_result_ball,name='result_ball'),
    path('ball/<id>',views.home_works_ball,name='ball'),
    # Delete
    path('delete/<int:id>/student/', views.delete_student, name='delete_student'),
    path('delete/<int:id>/group/', views.delete_group, name='delete_group'),
    path('delete/<int:id>/lesson/', views.delete_lesson, name='delete_lesson'),
    path('delete/<int:id>/home_work/', views.delete_home_work, name='delete_home_work'),
    path('delete/<int:id>/daily_material/', views.delete_daily_material, name='delete_daily_material'),
    path('lesson/<int:pk>/detail', LessonDetailView.as_view(), name='lesson_detail'),
    path('home_work/<int:id>/detail', views.home_work_detail, name='home_work_detail'),
    path('home_work/evaluation', HomeWorkEvaluationView.as_view(), name='home_work_evaluation'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)