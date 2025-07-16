from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.students_page, name='students'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('groups/', views.groups_page, name='groups'),
    path('groups/add/', views.add_group, name='add_group'),
    path('groups/delete/<int:group_id>/', views.delete_group, name='delete_group'),
    path('groups/edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('sessions/', views.sessions_page, name='sessions'),
    path('sessions/add/', views.add_session, name='add_session'),
    path('sessions/edit/<int:session_id>/', views.edit_session, name='edit_session'),
    path('sessions/delete/<int:session_id>/', views.delete_session, name='delete_session'),
    path('sessions/<int:session_id>/attendance/', views.attendance, name='attendance'),
    path('session/<int:session_id>/attendance/edit/', views.edit_attendance, name='edit_student_attendance'),
    path('payments/', views.payments_page, name='payments'),
    path('payments/add/<int:student_id>', views.add_payment, name='add_payment'),
    path('payments/download-csv/', views.download_payments_csv, name='download_payments_csv'),
    path('offers/create/', views.create_offer, name='create_offer'),
]
