from .models import *
from django import forms
from crispy_forms.helper import FormHelper


EXPERTIES_CHOICES = (('FrontEnd', 'Front-End'),
                     ('BackEnd', 'Back-End'),
                     ('FullStack', 'Full-Stack'),
                     ('DataScience', 'Data-Science'),
                     ('DataMining', 'Data-Mining'),
                     ('NewBie', 'NewBie'),
                     )

class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    phone_number = forms.CharField(max_length=10)

    class Meta:
        model = Admin
        fields = ('email', 'password', 'username', 'phone_number','profile_pic', 'designation', 'experties')
        widgets = {
            'experties' : forms.CheckboxSelectMultiple(choices=EXPERTIES_CHOICES)
        }

class ProjectForm(forms.ModelForm):
    discription = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Project
        exclude = ('is_deleted', 'slug', 'order')
       
       
class DateInput(forms.DateInput):
    input_type = 'date'

class IssueForm(forms.ModelForm):
    project_name = forms.Select()
    discription = forms.TextInput()
    class Meta:
        model = Issue
        exclude = ('is_deleted', 'slug', 'order')
 
       
        widgets = {
            'start_date' : DateInput(),
            'end_date' : DateInput()
           
        }
