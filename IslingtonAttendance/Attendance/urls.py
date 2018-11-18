from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('routines/', views.all_routines, name='all_routines'),
    path('routines/year/<year>', views.routines_by_year, name='routines_by_year'),
    path('modules/', views.all_modules, name='all_modules'),
    path('students/', views.all_students, name='all_students'),
    path('students/year/<year>', views.students_by_year, name='students_by_year'),
    path('students/faculty/<faculty>', views.students_by_faculty, name='students_by_faculty'),
    #path('student/<student_id>', views.student_view, name='student_view'),
    path('student/<student_id>', views.student_view2, name='student_view'),
    path('groups/', views.all_groups, name="all_groups"),
    path('groups/year/<year>', views.groups_by_year, name="groups_by_year"),
    path('groups/faculty/<faculty>', views.groups_by_faculty, name="groups_by_faculty"),
    path('groupsyear/<year>/<faculty>', views.groups_by_year_faculty, name="groups_by_year_faculty"),
    path('groupfaculty/<faculty>/<year>', views.groups_by_faculty_year, name="groups_by_faculty_year"),
    path('group/<group_id>/', views.group_view, name="group_view"),
    #path('attendance/<routine_id>/', views.attendance_by_routine, name="module_attendance_view"),
    path('attendance/<routine_id>/', views.attendance_by_routine2, name="module_attendance_view"),
    #path('test/<routine_id>/', views.attendance_by_routine2, name="test"),
    #path('test/<student_id>/', views.student_view2, name="test"),
]

'''path('modules/<int:faculty>/', views.module_list,name="module_list"),
path('group/<int:faculty_group>/', views.group_list,name="group_list"),
path('students/<slug:student_group>/', views.student_list,name="student_list"),'''