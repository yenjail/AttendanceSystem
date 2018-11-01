# Generated by Django 2.1 on 2018-10-29 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0007_auto_20181029_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance_detail',
            name='attendance',
            field=models.ForeignKey(db_column='attendance', on_delete=django.db.models.deletion.CASCADE, to='Attendance.Attendance'),
        ),
        migrations.AlterField(
            model_name='attendance_detail',
            name='enrollno',
            field=models.ForeignKey(blank=True, db_column='enrollno', null=True, on_delete=django.db.models.deletion.CASCADE, to='Attendance.Student_Enrollment', to_field='enrollno'),
        ),
    ]
