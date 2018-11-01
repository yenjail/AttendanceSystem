from django.contrib import admin
from .models import Teacher, Module, Teacher_Module, Faculty, Faculty_Module, Group, Routine, Group_Routine, Classroom, Attendance, Attendance_detail, AttendanceLog, Fingerprint, Student_Enrollment, Student, Student_group, Student_module, Device

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Module)
admin.site.register(Teacher_Module)
admin.site.register(Faculty)
admin.site.register(Faculty_Module)
admin.site.register(Group)
admin.site.register(Routine)
admin.site.register(Group_Routine)
admin.site.register(Classroom)
admin.site.register(Attendance)
admin.site.register(Attendance_detail)
admin.site.register(AttendanceLog)
admin.site.register(Fingerprint)
admin.site.register(Student_Enrollment)
admin.site.register(Student)
admin.site.register(Student_group)
admin.site.register(Student_module)
admin.site.register(Device)
