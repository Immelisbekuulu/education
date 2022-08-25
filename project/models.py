from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


class StudyYear(models.Model):
    class Meta:
        verbose_name = "Учебный Год"
        verbose_name_plural = "Учебный Год"

    date = models.CharField(max_length=250, verbose_name="Год")

    def __str__(self):
        return str(self.date)


class Teacher(models.Model):
    class Meta:
        verbose_name = "Преподователь"
        verbose_name_plural = "Преподователь"

    surname = models.CharField(max_length=250, verbose_name="Фамилия")
    name = models.CharField(max_length=250, verbose_name="Имя")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Фото")
    tel_num = models.CharField(max_length=250, verbose_name="Телефонный номер")
    year_data = models.PositiveIntegerField(verbose_name="Год рождения")
    password = models.CharField(max_length=250, verbose_name="Пароль")

    def __str__(self):
        return self.name


class Student(models.Model):
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студент"
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    surname = models.CharField(max_length=250, verbose_name="Фамилия", blank=True,null=True)
    name = models.CharField(max_length=250, verbose_name="Имя")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Фото")
    tel_num = models.CharField(max_length=250, verbose_name="Телефонный номер", blank=True,null=True)
    year_data = models.PositiveIntegerField(verbose_name="Год рождения",blank=True,null=True)
    password = models.CharField(max_length=250, verbose_name="Пароль", blank=True,null=True)
    create_data = models.DateField(auto_now=True, verbose_name="Дата регистрации")

    def __str__(self):
        return str(self.user)


class Groups(models.Model):
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группа"

    title = models.CharField(max_length=250, verbose_name="Названия")
    study_year = models.ForeignKey(StudyYear, on_delete=models.CASCADE, verbose_name="Учебный Год")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподователь")
    create_data = models.DateField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title


class StudentGroup(models.Model):
    class Meta:
        verbose_name = "Студент группа"
        verbose_name_plural = "Студент группа"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name="Группа")
    create_data = models.DateField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return str(self.student)


class DailyMaterial(models.Model):
    class Meta:
        verbose_name = "Ежедневный матерял"
        verbose_name_plural = "Ежедневный матерял"

    tema = models.CharField(max_length=250, verbose_name="Тема")
    text = RichTextField(verbose_name="Текст")
    create_data = models.DateField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return self.tema


class Lesson(models.Model):
    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Урок"

    daily_material = models.ManyToManyField(DailyMaterial, verbose_name="Ежедневный матерял")
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name="Группа")
    create_data = models.DateField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return str(self.group)


class Comment(models.Model):
    class Meta:
        verbose_name = "Коментарии"
        verbose_name_plural = "Коментарии"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Урок")
    text = RichTextField(verbose_name="Текст")
    create_data = models.DateField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return str(self.student)


class HomeWork(models.Model):
    class Meta:
        verbose_name = "Домашняя работа"
        verbose_name_plural = "Домашняя работа"
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name="Группа")
    material = models.ForeignKey(DailyMaterial, on_delete=models.CASCADE, verbose_name='Материал')
    text = models.CharField(max_length=255, verbose_name="Домашняя работа")
    home_work = models.ManyToManyField(Lesson, verbose_name="Урок")

    create_data = models.DateField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return str(self.text)


class Attendence(models.Model):
    class Meta:
        verbose_name = "Посещаемость"
        verbose_name_plural = "Посещаемость"

    CHOICES = (
        ('Непришел', '-'),
        ('Пришел', '+')

    )
    studentGroup = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, verbose_name="Студент группа")
    check_student = models.CharField(max_length=300, choices=CHOICES, verbose_name="Отметка")
    create_data = models.DateField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return str(self.studentGroup)


class HomeWorkResult(models.Model):
    class Meta:
        verbose_name = "Готовая домашняя работа"
        verbose_name_plural = "Готовая домашняя работа"

    student = models.CharField(max_length=255, verbose_name='Ф.И.О')
    home_work = models.ForeignKey(HomeWork, on_delete=models.CASCADE, verbose_name="Д/З")
    print_home_work = RichTextField(verbose_name="Домашняя работа")
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name="Группа")
    create_data = models.DateField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return str(self.student)



class HomeWorkEvaluation(models.Model):
    class Meta:
        verbose_name = "Оценка домашнего задания"
        verbose_name_plural = "Оценка домашнего задания"

    fio = models.CharField(max_length=255, verbose_name='Ф.И.О')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name="Группа")
    ball = models.PositiveIntegerField(verbose_name="Бал", blank=True, null=True)
    create_data = models.DateField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return str(self.fio)


