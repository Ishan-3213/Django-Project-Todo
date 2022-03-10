from celery import shared_task
from .models import *
from .views import *
from todo.utils import *
from . import utils

@shared_task(bind=True)
def mail_to_project_manager(self, project_id):
    # print("id recieved.......---!!!", project_id)
    project = Project.objects.get(id = project_id)
    # print("perosno----------", project)
    person_id = project.assign_to.id
    # print("perosno----------", person_id)
    person = Admin.objects.get(id = person_id)
    print("before---utiuksssssssss-id----------")
    utils.sending_mail(self, person, project, issue=None)
    print("after---utiuksssssssss-id----------")
    return "Done"
    
@shared_task(bind=True)
def mail_to_developer(self, issue_id):
    # print("id recieved.......---!!!", issue_id)
    issue = Issue.objects.get(id = issue_id)
    # print("perosno----------", issue)
    person_id = issue.assign_to.id
    # print("perosno-id----------", person_id)
    person = Admin.objects.get(id = person_id)
    print("before---utiuksssssssss-id----------")
    project = None
    utils.sending_mail(self, person, project, issue)
    print("after---utiuksssssssss-id----------")
    return "Done"
