# Generated by Django 4.0.2 on 2022-02-07 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tudu', '0005_alter_issue_end_date_alter_issue_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='profile_pic',
            field=models.ImageField(upload_to='profile_pic/'),
        ),
    ]
