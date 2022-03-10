from .utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import *
from . import tasks
from .tasks import *

@receiver(pre_save, sender=Project)
def slug_field_for_project(sender, instance, created = False, **kwargs):
    if not instance.slug:
        print("slug is generated.. FOR Project..!!!!.!!!")
        instance.slug = unique_slug_generator(instance)

@receiver(pre_save, sender=Issue)
def slug_field_for_issue(sender, instance, created= False, **kwargs):
    if not instance.slug:
        print("slug is generated.. FOR Issueeee..!!!!.!!!")
        instance.slug = unique_slug_generator(instance)

@receiver(post_save, sender=Project)
def email_sending_to_manager(sender, instance, created = False, **kwargs):
    if created:
        project_id = instance.id
        print("getting to mail...", project_id)
        tasks.mail_to_project_manager.delay(project_id)
        print("E-mail has been sent..!!!")

@receiver(post_save, sender=Issue)
def email_sending_to_developer(sender, instance, created = False, **kwargs):
    if created:
        issue_id = instance.id
        print("getting to mail...", issue_id)
        tasks.mail_to_developer.delay(issue_id)
        print("E-mail has been sent..!!!")