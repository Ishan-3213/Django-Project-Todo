# Generated by Django 4.0.2 on 2022-02-06 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tudu', '0003_alter_admin_designation_alter_issue_attachments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='end_date',
            field=models.DateField(help_text='Enter in the format of YYYY-MM-DD'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='start_date',
            field=models.DateField(help_text='Enter in the format of YYYY-MM-DD'),
        ),
    ]