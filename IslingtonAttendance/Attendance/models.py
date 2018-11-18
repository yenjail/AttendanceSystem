from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Teacher(models.Model):
    teacher_type_choices = (('Lecturer','Lecturer'),('Tutor','Tutor'))
    teacher_id = models.AutoField(primary_key=True, max_length=10)
    firstname = models.CharField(max_length=50, default="")
    lastname = models.CharField(max_length=50, default="")
    teacher_type = models.CharField(max_length=10,choices=teacher_type_choices, default="")
    username = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.firstname+" "+self.lastname

class Module(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    module_code = models.CharField(max_length=10, null=True, blank=True)
    period = models.CharField(max_length=20, blank=True)
    year = models.CharField(max_length=25)
    credit = models.IntegerField()

    def __str__(self):
        return self.title

class Teacher_Module(models.Model):
    class_type_choices = (("Lecture","Lecture"),("Tutorial","Tutorial"),("Lab","Lab"),("Tutorial and Lab","Tutorial and Lab"))
    module = models.ForeignKey("Module", on_delete=models.CASCADE)
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE)
    class_type = models.CharField(max_length=20,choices=class_type_choices, default="")

    def __str__(self):
        return str(self.module)+", "+str(self.teacher)+", "+str(self.class_type)

class Faculty(models.Model):
    faculty_id = models.AutoField(primary_key=True, max_length=5)
    name = models.CharField(max_length=70)

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        return self.name

class Faculty_Module(models.Model):
    faculty = models.ForeignKey("Faculty", on_delete=models.CASCADE)
    module = models.ForeignKey("Module", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.faculty)+", "+str(self.module)

class Group(models.Model):
    group_id = models.CharField(primary_key=True, max_length=6)
    semester = models.IntegerField(null=False)
    year = models.CharField(null=False,max_length=5)
    faculty=models.ForeignKey("Faculty",on_delete=models.CASCADE)

    def __str__(self):
        return str(self.group_id)+", year"+str(self.year)

class Routine(models.Model):
    class_type_choices = (("Lecture","Lecture"),("Tutorial","Tutorial"),("Lab","Lab"))
    day_choices = (("Sunday", "Sunday"), ("Monday", "Monday"), ("Tuesday", "Tuesday"),("Wednesday", "Wednesday"), ("Thursday", "Thursday"), ("Friday", "Friday"))
    routine_id=models.AutoField(primary_key=True)
    startTime=models.TimeField()
    endTime=models.TimeField()
    day_of_the_week = models.CharField(max_length=10,choices=day_choices,default="")
    class_type = models.CharField(max_length=15,choices=class_type_choices, default="")
    module = models.ForeignKey("Module",on_delete=models.CASCADE)
    teacher = models.ForeignKey("Teacher",on_delete=models.CASCADE)
    location = models.ForeignKey("Classroom",on_delete=models.CASCADE)
    #group = models.ForeignKey("Group",on_delete=models.CASCADE)
    startDate=models.DateField(null=True,blank=True)

    def __str__(self):
        return str(self.module)+", "+str(self.class_type)+", "+str(self.day_of_the_week)+", "+str(self.startTime)+", "+str(self.module)+", "+str(self.teacher)

class Group_Routine(models.Model):
    routine = models.ForeignKey("Routine", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.routine)+", "+str(self.group)

class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    classroom_name = models.CharField(max_length=55)
    block = models.CharField(max_length=55)
    capacity = models.IntegerField()
    #device_id = models.IntegerField()

    def __str__(self):
        return self.classroom_name

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, db_column="classroom")
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, db_column="routine")

    def __str__(self):
        return str(self.classroom)+", "+str(self.routine)

class Attendance_detail(models.Model):
    attendance_detail_id = models.BigAutoField(primary_key=True)
    attendance = models.ForeignKey("Attendance", on_delete=models.CASCADE, db_column="attendance")
    enrollno = models.ForeignKey("Student_Enrollment", null=True, blank=True, to_field="enrollno", on_delete=models.CASCADE, db_column="enrollno")
    #enrollno = models.IntegerField()
    entry_datetime=models.DateTimeField(null=True, blank=True)
    #status=models.CharField(max_length=2,blank=True)
    #device_id=models.ForeignKey("Device", null=True, blank=True, on_delete=models.CASCADE)
    devicekey = models.ForeignKey("Device", null=True, blank=True, to_field="devicekey", on_delete=models.CASCADE, db_column="devicekey")

    def __str__(self):
        return str(self.enrollno)+" ,"+str(self.attendance)
    
class AttendanceLog(models.Model):
    enrollno = models.IntegerField()
    attdate = models.DateField()
    atttime = models.TimeField()
    verifytime = models.DateTimeField(blank=True, null=True)
    deviceid = models.IntegerField(blank=True, null=True)
    devicekey = models.ForeignKey("Device", null=True, blank=True, to_field="devicekey", on_delete=models.CASCADE, db_column="devicekey")
    remarks = models.CharField(max_length=255,default="None")
    attmode = models.IntegerField(default=0)
    verifytype = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.enrollno)+", "+str(self.attdate)+", "+str(self.atttime)

class Fingerprint(models.Model):
    enrollno = models.IntegerField()
    fingerprint = models.TextField()
    finger_number = models.IntegerField() #finger number starting from thumb finger of right hand

    def __str__(self):
        return str(self.enrollno)

    class Meta:
        verbose_name_plural = "Fingerprints"

class Student_Enrollment(models.Model):
    student = models.ForeignKey("Student",on_delete=models.CASCADE)
    enrollno = models.IntegerField(unique=True)
    effective_date = models.DateField()

    def __str__(self):
        return str(self.student)+", "+str(self.enrollno)

class Student(models.Model):
    gender_choices = (("Male","Male"),("Female","Female"),("Other","Other"))
    student_id = models.CharField(primary_key=True, max_length=16)
    #group = models.ForeignKey("Group",on_delete=models.CASCADE);
    student_first_name = models.CharField(max_length=50)
    student_last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10,choices=gender_choices,blank=True)
    email = models.EmailField(max_length=254,blank=True)
    contact = models.CharField(max_length=15,blank=True)
    current_address = models.CharField(max_length=95,blank=True)
    permanent_address = models.CharField(max_length=95,blank=True)
    #photo = models.CharField(max_length=255, null=True)
    #enroll_no=models.ForeignKey("Fingerprints",on_delete=models.CASCADE)
    #qr_code=models.CharField(max_length=255,blank=True)
    #nfc=models.CharField(max_length=255,blank=True)
    #barcode=models.CharField(max_length=255,blank=True)

    def __str__(self):
        return str(self.student_id) + ", " + str(self.student_first_name)+ ", " +str(self.student_last_name)

class Student_group(models.Model):
    student = models.ForeignKey("Student",on_delete=models.CASCADE)
    group = models.ForeignKey("Group",on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=50)

    def __str__(self):
        return str(self.student)+", "+str(self.academic_year)+", "+str(self.group)

class Student_module(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    module = models.ForeignKey("Module", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student)+", "+str(self.module)

'''class Device(models.Model):
    device_id = models.IntegerField(primary_key=True)
    device_ip = models.CharField(max_length=100)
    location = models.ForeignKey("Classroom", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.device_id)+", "+str(self.location)'''
    
class Device(models.Model):
    deviceid = models.IntegerField(primary_key=True)
    devicename = models.CharField(max_length=100)
    deviceip = models.CharField(max_length=50)
    devicekey = models.CharField(max_length=255,unique=True)
    location = models.ForeignKey("Classroom", on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.deviceid)+", "+str(self.devicekey)+", "+str(self.location)
    