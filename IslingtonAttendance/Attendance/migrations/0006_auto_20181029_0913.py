# Generated by Django 2.1 on 2018-10-29 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0005_auto_20181029_0912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student_enrollment',
            old_name='enroll_no',
            new_name='enrollno',
        ),
    ]