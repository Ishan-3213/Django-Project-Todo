# Generated by Django 4.0.2 on 2022-02-08 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tudu', '0006_alter_admin_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='designation',
            field=models.CharField(choices=[('Developer', 'Developer'), ('Project-Manager', 'Project-Manager'), ('Admin', 'Admin')], default='Admin', max_length=50),
        ),
    ]
