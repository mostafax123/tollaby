from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum
from django.contrib import messages
from django.http import HttpResponse
import csv
from .forms import StudentForm, GroupForm, SessionForm
from .models import *

def dashboard(request):
    students = Student.objects.all()
    sessions = Session.objects.all()
    groups = Group.objects.all()
    revenue = Payment.objects.aggregate(Sum('amount_paid'))
    context = {
        "no_students": students.count(),
        "no_sessions": sessions.count(),
        "no_groups": groups.count(),
        "revenue": revenue,
    }
    return render(request, 'index.html', context)

def students_page(request):
    students = Student.objects.values(
        "id",
        "name",
        "group__grade",
        "phone_number",
        "sex",
        "group__name",
        "offer__title"
    )
    groups = Group.objects.all()
    offers = Offer.objects.all()
    context = {
        "students": students,
        "groups": groups,
        "offers": offers,
    }
    return render(request, 'students/students_list.html', context)

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully")
            return redirect('students')
        else:
            messages.error(request, "Invalid form")
    form = StudentForm()
    context = {'form': form}
    return render(request, 'students/add_student.html', context)

def delete_student(request, student_id):
    student = Student.objects.get(pk=student_id)
    student.delete()
    return redirect('students')

def edit_student(request, student_id):
    student = Student.objects.get(pk=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student edited successfully")
            return redirect('students')
        else:
            messages.error(request, "Invalid form")
            return redirect('students')

    form = StudentForm(instance=student)
    return render(request, 'students/edit_student.html', {"form": form})

def groups_page(request):
    groups = Group.objects.all()
    no_group_students = Student.objects.values("group_id").annotate(students_count=Count("group_id"))
    context = {
        "groups": zip(groups, no_group_students),
    }
    return render(request, 'groups/groups_list.html', context)

def add_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Group added successfully")
            return redirect('groups')
        else:
            messages.error(request, "Invalid form")

    form = GroupForm()
    return render(request, 'groups/add_group.html', {"form": form})

def delete_group(request, group_id):
    student = Group.objects.get(pk=group_id)
    student.delete()
    return redirect('groups')

def edit_group(request, group_id):
    group = Group.objects.get(pk=group_id)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Group edited successfully")
            return redirect('groups')
        else:
            messages.error(request, "Invalid form")
            return redirect('groups')

    form = GroupForm(instance=group)
    return render(request, 'groups/edit_group.html', {"form": form})

def sessions_page(request):
    sessions = Session.objects.values(
        "id",
        "title",
        "duration",
        "group__grade",
        "price",
        "group__name",
        "date"
    )
    context = {
        "sessions": sessions,
    }
    return render(request, 'sessions/sessions_list.html', context)

def add_session(request):
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Session added successfully")
            return redirect('sessions')
        else:
            messages.error(request, "Invalid form")

    form = SessionForm()
    return render(request, 'sessions/add_session.html', {"form": form})

def edit_session(request, session_id):
    session = Session.objects.get(pk=session_id)
    if request.method == "POST":
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Session edited successfully")
            return redirect('sessions')
        else:
            messages.error(request, "Invalid form")
            return redirect('sessions')

    form = SessionForm(instance=session)
    return render(request, 'sessions/edit_session.html', {"form": form})

def delete_session(request, session_id):
    session = Session.objects.get(pk=session_id)
    session.delete()
    return redirect('sessions')


def attendance(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    students = session.group.student_set.all()
    for student in students:
        Attendance.objects.get_or_create(student=student, session=session)
    attendance = Attendance.objects.filter(session=session)
    context = {'attendance': attendance, 'session': session}
    return render(request, 'attendance/take_attendance.html', context)


def edit_attendance(request, session_id):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        student_attendance = Attendance.objects.get(student=student_id, session=session_id)
        student_attendance.is_attendant = not student_attendance.is_attendant
        student_attendance.save()
        return redirect('attendance', session_id=session_id)


def calc_amount_due(student):
    amount_due = student.attendance_set.filter(is_attendant=True).aggregate(Sum('session__price'))
    offer = student.offer.discount
    print(offer)
    return amount_due['session__price__sum'] - (amount_due['session__price__sum'] * (offer/100))

def payments_page(request):
    students = Student.objects.all()
    for student in students:
        Payment.objects.get_or_create(student=student)
        student_payment = Payment.objects.get(student=student)
        if student.attendance_set.filter(is_attendant=True).exists():
            student_payment.amount_due = calc_amount_due(student)
        else:
            student_payment.amount_due = 0
        student_payment.save()

    payments = Payment.objects.values(
        "student_id",
        "student__name",
        "student__group__grade",
        "amount_due",
        "amount_paid",
        "last_payment"
    )
    context = {
        "payments": payments,
    }
    return render(request, 'payments/payments_list.html', context)

def add_payment(request, student_id):
    student_payment = Payment.objects.get(student=student_id)
    if request.method == "POST":
        student_payment.amount_paid += int(request.POST.get("amount"))
        student_payment.last_payment = request.POST.get("amount")
        student_payment.save()
        return redirect('payments')
    return render(request, 'payments/add_payment.html')

def create_offer(request):
    if request.method == "POST":
        name = request.POST.get("name")
        discount = request.POST.get("discount")
        Offer.objects.create(title=name, discount=discount)
        return redirect('students')
    return render(request, 'create_offer.html')

def download_payments_csv(request):
    # Get all students and ensure they have payment records
    students = Student.objects.all()
    for student in students:
        Payment.objects.get_or_create(student=student)
        student_payment = Payment.objects.get(student=student)
        if student.attendance_set.filter(is_attendant=True).exists():
            student_payment.amount_due = calc_amount_due(student)
        else:
            student_payment.amount_due = 0
        student_payment.save()

    # Get payment data
    payments = Payment.objects.values(
        "student_id",
        "student__name",
        "amount_due",
        "amount_paid",
        "last_payment"
    )

    # Create the HttpResponse object with CSV header
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="payments.csv"'},
    )

    # Create CSV writer
    writer = csv.writer(response)

    # Write header row
    writer.writerow(['الطالب', 'المبلغ المستحق', 'المبلغ المدفوع', 'المتبقي', 'آخر دفعة'])

    # Write data rows
    for payment in payments:
        writer.writerow([
            payment['student__name'],
            payment['amount_due'],
            payment['amount_paid'],
            payment['amount_due'] - payment['amount_paid'],
            payment['last_payment']
        ])

    return response
