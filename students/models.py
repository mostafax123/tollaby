from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

GRADES = (
        ('الصف السادس الابتدائي', 'الصف السادس الابتدائي'),
        ('الصف الأول الاعدادي', 'الصف الأول الاعدادي'),
        ('الصف الثاني الاعدادي', 'الصف الثاني الاعدادي'),
        ('الصف الثالث الاعدادي', 'الصف الثالث الاعدادي'),
        ('الصف الأول الثانوي', 'الصف الأول الثانوي'),
        ('الصف الثاني الثانوي', 'الصف الثاني الثانوي'),
        ('الصف الثالث الثانوي', 'الصف الثالث الثانوي'),
        ('بدون صف محدد', 'بدون صف محدد')
)

SEX = (('ذكر', 'ذكر'), ('أنثي', 'أنثي'))

class Student(models.Model):
    name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(max_length=13, unique=True)
    sex = models.CharField(max_length=20, choices=SEX)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Offer(models.Model):
    title = models.CharField(max_length=255)
    discount = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.title

class Group(models.Model):
    name = models.CharField(max_length=255)
    grade = models.CharField(max_length=21, choices=GRADES)

    def __str__(self):
        return self.name

class Session(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    duration = models.FloatField()
    price =models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    is_attendant = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name}, {self.session.title}"

    class Meta:
        unique_together = ('student', 'session')

class Payment(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    amount_due = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    amount_paid = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    last_payment = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    last_payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} amount due: {self.amount_due}"
