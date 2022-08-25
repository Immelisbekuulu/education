import secrets

from project.models import StudentGroup, Groups, HomeWork, Lesson, Attendence, HomeWorkResult, Student, StudyYear, \
    DailyMaterial
import string

def get_studentgroup():
    return StudentGroup.objects.all()

def get_groups():
    return Groups.objects.all()

def get_students():
    return Student.objects.all()

def get_students_goup_by_id(id):
    return StudentGroup.objects.get(group=id)

def students_password():
    alphabet = string.ascii_lowercase + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))
    return password

def get_home_work():
    return HomeWork.objects.all()

def students_attendence():
    return Attendence.objects.all()

def study_year():
    return StudyYear.objects.all()

def lessons_objects():
    return Lesson.objects.all()

def daily_material_objects():
    return DailyMaterial.objects.all()

def get_students_attendence():
    return Attendence.objects.all()

def get_groups_id():
    return Groups.objects.get(id=id)

def filter_students_group():
    return StudentGroup.objects.filter(group=id)

def get_students_groups_first():
    return StudentGroup.objects.filter(group=id).first()

def get_groups_lesson(id):
    return Lesson.objects.filter(group=id)

def filter_groups_lesson(id):
    return Lesson.objects.filter(group=id).first()

def get_lessons_home_work(id):
    lesson2 = Lesson.objects.filter(group=id).first()
    return HomeWork.objects.filter(lesson=lesson2)

def filter_students_attendence(id):
    studentGroup2 = StudentGroup.objects.filter(group=id).first()
    return Attendence.objects.filter(studentGroup=studentGroup2)

def home_works_result():
    return HomeWorkResult.objects.all()
