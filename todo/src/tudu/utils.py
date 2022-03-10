import random
import string
from django.utils.text import slugify

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def sending_mail(self, person, project, issue):
    """
    This function is for sending mail to the project/issue assigned person...!!
    
    """
    subject = "Your Assignment have arrived...!!!"
    template_name = 'adminportal/email.html'
    html_message = render_to_string(template_name, {"project": project, "person":person, "issue": issue})
    plain_message = strip_tags(html_message)
    from_mail = settings.EMAIL_HOST_USER
    to_email = [person.email]
    send_mail(subject, plain_message, from_mail, to_email, html_message=html_message )