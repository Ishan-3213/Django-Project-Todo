from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import  RegexValidator
from django.contrib.auth.models import  AbstractUser
from generic.models import *

# Create your models here.
DESIGNATION_CHOICE = (('Developer', 'Developer'),
                      ('Project-Manager' , 'Project-Manager'),
                      ('Admin', 'Admin'))

class Admin(BaseModel, AbstractUser):

    profile_pic = models.ImageField(upload_to = "profile_pic/")
    phone_regex = RegexValidator(regex=r'^[7-9]{1}\d{9}', message="Phone number must start with '9999999999'")
    phone_number = models.CharField(validators=[phone_regex], help_text=_('Enter Number in format: "9999999999"') , max_length=10, blank=True, unique=True) 
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICE, default = "Admin")
    email = models.EmailField(max_length=150,unique=True)
    experties = models.CharField(max_length=256, null= True)

    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Admin'
        db_table = "admin"

    def __str__(self):
        return self.username

STATUS_CHOICE = (('NotStarted', 'NotStarted'),
                 ('Pending', 'Pending'),               
                 ('Completed', 'Completed'))

class Project(BaseModel):

    assign_to = models.ForeignKey(Admin, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    discription = models.TextField()
    slug = models.SlugField(max_length=256, blank=True ,null=True)
    status = models.CharField(max_length=20, choices= STATUS_CHOICE)
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse_lazy("tudu:project_detail", kwargs={"slug": self.slug})
    
DIFFICULTY_CHOICE = (('High', 'High'),
                     ('Medium','Medium'),
                     ('Low', 'Low'))

class Issue(BaseModel):
    
    project_name = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=10) 
    title = models.CharField(max_length=200)
    discription = models.CharField(max_length=300, null=True, blank=True)
    slug = models.SlugField(max_length=256, blank=True, null=True) 
    priority = models.CharField(max_length=20, choices=DIFFICULTY_CHOICE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE)
    assign_to = models.ForeignKey(Admin, null=True,  on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICE)
    attachments = models.ImageField(upload_to = "issues_image", null = True, blank = True)
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("tudu:issue_detail", kwargs={"slug":self.project_name.slug, "pk": self.id})



