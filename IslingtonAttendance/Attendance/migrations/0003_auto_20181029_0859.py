# Generated by Django 2.1 on 2018-10-29 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0002_auto_20181029_0833'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance_detail',
            old_name='enroll_no',
            new_name='enrollno',
        ),
        migrations.RenameField(
            model_name='attendancelog',
            old_name='enroll_no',
            new_name='enrollno',
        ),
        migrations.RenameField(
            model_name='fingerprint',
            old_name='enroll_no',
            new_name='enrollno',
        ),
    ]
