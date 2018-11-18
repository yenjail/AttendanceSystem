from django.shortcuts import render
from .models import Student_group, Group, Attendance, Routine, Student, Faculty, AttendanceLog, Device, Student_Enrollment

def all_students(request):
    #students = Student.objects.all()
    faculties = Faculty.objects.all()
    years = (1,2,3)
    students = Student_group.objects.all()
    return render(request, 'Attendance/student_list.html',{'students':students,
                                                           'faculties':faculties,
                                                           'years':years})

def students_by_year(request,year):
    students = Student_group.objects.filter(group__year=year)
    return render(request, 'Attendance/student_list_year.html',{'students':students,
                                                           'year':year})
    
def students_by_faculty(request,faculty):
    students = Student_group.objects.filter(group__faculty__name=faculty)
    return render(request, 'Attendance/student_list_faculty.html',{'students':students,
                                                           'faculty':faculty})

def group_view(request,group_id):
    students = Student_group.objects.filter(group = group_id)
    return render(request, 'Attendance/group_student_list.html',{'students':students,
                                                                 'group':group_id})

def all_groups(request):
    groups = Group.objects.all()
    years = (1,2,3)
    faculties = Faculty.objects.all()
    return render(request, 'Attendance/group_list.html',{'groups':groups,
                                                         'years':years,
                                                         'faculties':faculties})

def groups_by_year(request,year):
    groups = Group.objects.filter(year=year)
    faculties = Faculty.objects.all()
    return render(request, 'Attendance/group_list_year.html',{'groups':groups,
                                                              'year':year,
                                                              'faculties':faculties})

def groups_by_faculty(request,faculty):
    groups = Group.objects.filter(faculty__name=faculty)
    years = (1,2,3)
    return render(request, 'Attendance/group_list_faculty.html',{'groups':groups,
                                                              'faculty':faculty,
                                                              'years':years})
    
def groups_by_year_faculty(request,year,faculty):
    groups = Group.objects.filter(faculty__name=faculty,year=year)
    years = (1,2,3)
    faculties = Faculty.objects.all()
    return render(request, 'Attendance/group_list_year_faculty.html',{'groups':groups,
                                                         'faculty':faculty,
                                                         'year':year,
                                                         'years':years,
                                                         'faculties':faculties})
    
def groups_by_faculty_year(request,faculty,year):
    groups = Group.objects.filter(faculty__name=faculty,year=year)
    years = (1,2,3)
    faculties = Faculty.objects.all()
    return render(request, 'Attendance/group_list_faculty_year.html',{'groups':groups,
                                                         'faculty':faculty,
                                                         'year':year,
                                                         'years':years,
                                                         'faculties':faculties})

def all_modules(request):
    attendances = Attendance.objects.all()
    return render(request, 'Attendance/attendance_module.html', {'attendances':attendances})

def attendance_by_module(request,module_id):
    attendances = Attendance.objects.filter(rountine=module_id)
    return render(request, 'Attendance/attendance_module.html', {'attendances':attendances})

def all_routines(request):
    routines = Routine.objects.all()
    years = (1,2,3)
    return render(request, 'Attendance/routine_list.html', {'routines':routines,
                                                            'years':years})

def routines_by_year(request,year):
    routines = Routine.objects.filter(module__year=year)
    return render(request, 'Attendance/routine_list_year.html', {'routines':routines,
                                                                 'year':year})

def index(request):
    groups = Group.objects.all()
    students = Student.objects.all()
    routines = Routine.objects.all()
    return render(request, 'Attendance/index2.html', {'groups':groups,
                                                     'students':students,
                                                     'routines':routines})

def attendance_by_routine_rough(request,routine_id):
    import numpy as np
    routine = Routine.objects.get(routine_id=routine_id)
    groups = routine.group_routine_set.all()
    attendance = routine.attendance_set.all()[0]
    attendance_details = attendance.attendance_detail_set.all()
    unique_days = attendance_details.distinct("entry_datetime")
    days = [day.entry_datetime.date() for day in unique_days]
    attendances_by_day = [[attendance_details.filter(entry_datetime__date=d)] for d in days]
    enrolls = attendance_details.distinct("enrollno")
    students = [enroll.enrollno.student for enroll in enrolls]
    attendances_dict = {}
    for student in students:
        attendances_dict[student] = []
    for at in attendances_by_day:
        for att in at:
            for a in att:
                attendances_dict[a.enrollno.student].append(a.entry_datetime.time())
    attendances_list = np.concatenate((np.array([list(attendances_dict.keys())]).T,list(attendances_dict.values())),axis=1)
    return render(request, 'Attendance/attendance_module2.html', {'attendance':attendance,
                                                                 'attendance_details':attendance_details,
                                                                 'groups':groups,
                                                                 'days':days,
                                                                 'attendances_by_day':attendances_by_day,
                                                                 'students':students,
                                                                 'attendances_list':attendances_list,
                                                                 'attendances_dict':attendances_dict
                                                                 })
    
def attendance_by_routine(request,routine_id):
    routine = Routine.objects.get(routine_id=routine_id)
    groups = routine.group_routine_set.all()
    attendance = routine.attendance_set.all()[0]
    attendance_details = attendance.attendance_detail_set.all()
    unique_days = attendance_details.distinct("entry_datetime__date")
    days = [day.entry_datetime.date() for day in unique_days]
    attendances_by_day = [[attendance_details.filter(entry_datetime__date=d)] for d in days]
    enrolls = attendance_details.distinct("enrollno")
    students = [enroll.enrollno.student for enroll in enrolls]
    attendances_dict = {}
    for student in students:
        attendances_dict[student] = [student.student_group_set.all()[0].group_id]
    i = 1
    for at in attendances_by_day:
        for att in at:
            i+=1
            for a in att:
                attendances_dict[a.enrollno.student].append(a.entry_datetime.time())
            for key,value in attendances_dict.items():
                if len(value) != i:
                    attendances_dict[key].append("Absent")
    return render(request, 'Attendance/attendance_module2.html', {'attendance':attendance,
                                                                 'groups':groups,
                                                                 'days':days,
                                                                 'attendances_dict':attendances_dict
                                                                 })
    
def attendance_by_routine2(request,routine_id):
    import datetime
    routine = Routine.objects.get(routine_id=routine_id)
    groups = routine.group_routine_set.all()
    location = routine.location #get classroom of routine
    device = Device.objects.get(location=location) #get device located in the classroom
    startTime = routine.startTime #starttime or routine
    endTime = (datetime.datetime.combine(datetime.date(1, 1, 1), routine.endTime) - datetime.timedelta(minutes=30)).time() #end time of routine minus some time delta
    logs = AttendanceLog.objects.filter(devicekey=device.devicekey).filter(atttime__range=(startTime,endTime)) # get all attendance logs from the particular device entered between startTime and endTime
    unique_days = logs.distinct("attdate")
    days = [day.attdate for day in unique_days]
    attendances_by_day = [[logs.filter(attdate=d)] for d in days]
    enrolls = logs.distinct("enrollno")
    students = [Student_Enrollment.objects.get(enrollno=enroll.enrollno).student for enroll in enrolls]
    attendances_dict = {}
    for student in students:
        attendances_dict[student] = [student.student_group_set.all()[0].group_id]
    i = 1
    for at in attendances_by_day:
        for att in at:
            i+=1
            for a in att:
                attendances_dict[Student_Enrollment.objects.get(enrollno=a.enrollno).student].append(a.atttime)
            for key,value in attendances_dict.items():
                if len(value) != i:
                    attendances_dict[key].append("Absent")
    return render(request, 'Attendance/attendance_module3.html', {'routine':routine,
                                                    'groups':groups,
                                                    'days':days,
                                                    'attendances_dict':attendances_dict})
    
def student_view2(request,student_id):
    student = Student.objects.get(student_id=student_id)
    group = student.student_group_set.all()[0]
    enrolled_modules = student.student_module_set.all()
    routines = group.group.group_routine_set.all()
    enrollno = student.student_enrollment_set.all()[0].enrollno
    logs = []
    import datetime
    for i in range(len(routines)):
        location = routines[i].routine.location #get location of the
        device = Device.objects.get(location=location) #get the associated device
        startTime = routines[i].routine.startTime #starttime or routine
        endTime = (datetime.datetime.combine(datetime.date(1, 1, 1), routines[i].routine.endTime) - datetime.timedelta(minutes=30)).time() #end time of routine minus some time delta
        log = AttendanceLog.objects.filter(devicekey=device.devicekey).filter(atttime__range=(startTime,endTime)).filter(enrollno=enrollno) # get all attendance logs from the particular device entered between startTime and endTime
        logs.append(log)
    unique_days = [log.distinct('attdate') for log in logs]
    days = [[day.attdate for day in u] for u in unique_days]
    attendances_dict = {}
    for i in range(len(list(routines))):
        atts = []
        for day in days[i]:
            for atts_detail in logs[i]:
                if day == atts_detail.attdate:
                    atts.append((day,atts_detail.atttime))
                    break
            else:
                atts.append((day,"Absent"))
        attendances_dict[routines[i]] = atts 
    return render(request, 'Attendance/student.html', {"student":student,
                                                       'group':group,
                                                       'enrolled_modules':enrolled_modules,
                                                       'attendances_dict':attendances_dict
                                                       })
    
def student_view_rough(request,student_id):
    student = Student.objects.get(student_id=student_id)
    group = student.student_group_set.all()[0]
    enrolled_modules = student.student_module_set.all()
    routines = group.group.group_routine_set.all()
    attendances = [r.routine.attendance_set.all() for r in routines]
    #for a in attendances:
    #    attendance_detail = a[0].attendance_detail_set.all()
    attendance_details = [a[0].attendance_detail_set.filter(enrollno__student__student_id=student_id) for a in attendances]
    #attendances_dict = {routines[0]:attendance_details[0]}
    attendances_dict = {}
    for i in range(len(list(routines))):
        attendances_dict[routines[i]] = attendance_details[i]
    
    '''for detail in attendance_details:
        unique_days = detail.distinct("entry_datetime__date")
        days = [day.entry_datetime.date() for day in unique_days]'''
    return render(request, 'Attendance/student.html', {"student":student,
                                                       'group':group,
                                                       'enrolled_modules':enrolled_modules,
                                                       'routines':routines,
                                                       'attendances':attendances,
                                                       'attendance_details':attendance_details,
                                                       'attendances_dict':attendances_dict
                                                       })
    
def student_view(request,student_id):
    student = Student.objects.get(student_id=student_id)
    group = student.student_group_set.all()[0]
    enrolled_modules = student.student_module_set.all()
    routines = group.group.group_routine_set.all()
    attendances = [r.routine.attendance_set.all() for r in routines]
    attendance_details_ = [a[0].attendance_detail_set.all() for a in attendances]
    unique_days = [a.distinct("entry_datetime__date") for a in attendance_details_]
    days = [[day.entry_datetime.date() for day in u] for u in unique_days]
    attendance_details = [a[0].attendance_detail_set.filter(enrollno__student__student_id=student_id) for a in attendances]
    attendances_dict = {}
    for i in range(len(list(routines))):
        atts = []
        for day in days[i]:
            for atts_detail in attendance_details[i]:
                if day == atts_detail.entry_datetime.date():
                    atts.append((day,atts_detail.entry_datetime.time()))
                    break
            else:
                atts.append((day,"Absent"))
        attendances_dict[routines[i]] = atts 
        #attendances_dict[routines[i]] = attendance_details[i]
    return render(request, 'Attendance/student.html', {"student":student,
                                                       'group':group,
                                                       'enrolled_modules':enrolled_modules,
                                                       'attendances_dict':attendances_dict,
                                                       'attendance_details':attendance_details,
                                                       })

'''def student_list(request):
	students = Student.objects.all()
	groups = Group.objects.all()
	return render(request, 'Attendance/student_list.html',{'students' : students, 'groups' : groups})

def module_list(request):
	modules = Module.objects.all()
	return render(request, 'Attendance/module_list.html',{'modules' : modules})

def login_page(request):
	return(request,'Attenadnce/login_page.html')

# Create your views here.

def faculty(request):
    faculties=Faculty.objects.all()
    return render(request, 'faculty.html', {'faculties': faculties})

def module_list(request,faculty):
    modules = Faculty_Module_Group.objects.prefetch_related('module').filter(faculty_id=faculty)
    # mods = modules[0].faculty_id
    # mods = Faculty_Module_Group.objects.prefetch_related('module_id').prefetch_related('student_id').filter

    return render(request,'modules.html', {'modules':modules})

def group_list(request,faculty_group):
    group=Group.objects.filter(faculty_id=faculty_group)

    return render(request, 'group.html', {'groups':group})

def student_list(request,student_group):
    students=Student_group.objects.prefetch_related('student').filter(group=student_group)

    return render(request,'student_record.html',{'student':students})
'''