from django import forms
from django.forms import modelformset_factory

from .models import *


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        labels = {
            'name': "اسم الطالب",
            'phone_number': 'رقم موبايل ولي الأمر',
            'sex': 'النوع',
            'group': 'المجموعة',
            'offer': 'نوع الخصم'
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        labels = {
            'name': 'اسم المجموعة',
            'grade': 'الصف'
        }

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = '__all__'
        labels = {
            'title': 'عنوان الخصم',
            'discount': 'نسبة الخصم'
        }

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = '__all__'
        labels = {
            'title': 'عنوان الحصة',
            'duration': 'المدة',
            'price': 'السعر (بالجنيه)',
            'group': 'المجموعة',
            'date': 'تاريخ الحصة'
        }

        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['amount_due', 'amount_paid', 'last_payment_date']