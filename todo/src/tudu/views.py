from django.urls import reverse_lazy
from django.views.generic import *
from generic.views import *
from django.db.models import Q
from .forms import *
from .models import *
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline

#-------------------For the pdf generation.-------------------------#
from django.http import FileResponse, JsonResponse
import io
from datetime import  datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from textwrap import wrap

#--------------------------------Home View---------------------------#

class HomeView(BasicListView):
    model = Project
    template_name = 'adminportal/index.html'
    context_object_name = 'items'
    

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Project.objects.all()
        return queryset


class SearchView(BasicListView):
    model = Admin
    template_name = 'adminportal/search.html'
    context_object_name ='search'

    def get_queryset(self):
        issues = self.request.GET.get('issues', None)
        projects = self.request.GET.get('projects', None)
        users = self.request.GET.get('users', None)
        print("Searched-------------->", issues, projects, users)
       
        if issues:
            vector = SearchVector('title','project_name__title','project_name__status', 'discription','assign_to__username','assign_to__designation', 'status')
            query = SearchQuery(issues)
            queryset = Issue.objects.annotate(search=vector).filter(search=query)
        elif projects:
            vector = SearchVector('title','status', 'discription','assign_to__username','assign_to__designation')
            query = SearchQuery(projects)
            queryset = Project.objects.annotate(search=vector).filter(search=query)
        elif users:
            vector = SearchVector('username','designation', 'username__assign_to__title')
            query = SearchQuery(users)
            queryset = Admin.objects.annotate(search=vector).filter(search=query)
        else:
            queryset = None
        return queryset


#--------------------------------Admin CRUD---------------------------#

class AdminRegistrationView(PermissionRequiredMixin, FormView):
    model = Admin
    form_class = AdminForm
    template_name = 'adminportal/registration.html'
    raise_exception = True
    permission_required = 'user.designation.Admin'
    redirect_field_name = 'next' 

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name()) 

        if not self.has_permission():
            return redirect('/sorry-not-allowed/')
        return super(AdminRegistrationView, self).dispatch(request, *args ,**kwargs)    


    def form_valid(self, form):
        user = form.save()
        user.set_password(user.password)
        # group = Group.object.get(name = 'Admin')
        # user.groups.add(group)
        user.save()    
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tudu:index')


class UserListView(BasicListView):

    model = Admin
    template_name = 'adminportal/user.html'
    context_object_name = 'user_data'
    ordering = 'designation'

class UserUpdateView(BasicUpdateView):
    model = Admin
    form_class = AdminForm
    template_name = 'adminportal/update.html'

    def form_valid(self, form):
        user = form.save()
        user.set_password(user.password)
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        print("form updated successfully....---!!!")
        return reverse_lazy("tudu:users")

class UserDeleteView(BasicDeleteView):
    model = Admin
    template_name = 'adminportal/proddel.html'
    context_object_name = 'delete_product'

    def get_success_url(self):
        print("form Deleted successfully....---!!!")
        return reverse_lazy("tudu:users")

class UserDetailView(BasicDetailView):
    model = Admin
    template_name = "adminportal/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_user'] = Project.objects.filter(Q(assign_to__username = self.object.username))
        context['issue_user'] = Issue.objects.filter(Q(assign_to__username = self.object.username))
        return context

#--------------------------------Project CRUD---------------------------#

class ProjectCreateView(BasicCreateView):

    model = Project
    form_class = ProjectForm
    template_name = 'adminportal/project_creation.html'

     
    def get_success_url(self):
        return reverse_lazy('tudu:index')

class ProjectDetailView(BasicDetailView):
    model = Project
    template_name = "adminportal/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Issue.objects.filter(Q(project_name__title = self.object.title)).order_by('-status')
        return context

class ProjectUpdateView(BasicUpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "adminportal/update.html"

    def get_success_url(self):
        print("form updated successfully....---!!!")
        return reverse_lazy("tudu:index")

class ProjectDeleteView(BasicDeleteView):
    model = Project
    template_name = "adminportal/proddel.html"
    context_object_name = 'delete_product'

    def get_success_url(self):
        print("form Deleted successfully....---!!!")
        return reverse_lazy("tudu:index")

#--------------------------------Issue CRUD---------------------------#

class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'adminportal/issue_creation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = Project.objects.get(slug=self.kwargs['slug'])
        return context

    def get_initial(self):
        self.user_name = self.request.user.designation
        if self.user_name == "Developer":
            # print("-------usenmae------->>", self.user_name, type(self.user_name))
            self.slug = Project.objects.get(slug=self.kwargs['slug'])
            # print("slugg---------", self.slug)
            self.user_assign = self.request.user
            initial = {'project_name' : self.slug, "assign_to": self.user_assign}
        else:
            self.slug = Project.objects.get(slug=self.kwargs['slug'])
            # print("slugg---------", self.slug)
            initial = {'project_name' : self.slug, "issue_type": "None"}
        return initial

    def get_success_url(self):
        project_slug = self.kwargs['slug']
        project = Project.objects.get(slug=project_slug)
        # print("Self------------Slug", project.slug)
        return reverse_lazy('tudu:project_detail', kwargs = {'slug':project.slug})
        
class IssueListView(BasicListView):
    
    model = Issue
    template_name = 'adminportal/issue_page.html'
    context_object_name = 'issues'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Issue.objects.all()
        return queryset


class IssueDetailView(BasicDetailView):
    model = Issue
    template_name = "adminportal/issue_detail.html"

class IssueUpdateView(BasicUpdateView):

    model = Issue
    form_class = IssueForm
    template_name = "adminportal/update.html"

    def get_initial(self):
        self.slug = self.kwargs['slug']
        # print("slug---------------------", self.slug)
        self.project_id = Issue.objects.get(slug=self.slug)
        self.proj_name = self.project_id.project_name
        # self.name = Project.objects.get(title = self.proj_name)
        # print("slug---------Project instance????------------", self.name, type(self.name))
        initial = {'project_name' : self.proj_name}
        return initial

    def get_success_url(self):
        self.project_issue = self.kwargs['slug']
        # print("Self---Slug", self.project_issue)
        proj = Issue.objects.get(slug = self.project_issue)
        project = proj.project_name.slug
        # print("Final slug---------------------------", project)
        return reverse_lazy('tudu:project_detail', kwargs = {'slug':project})

class IssueDeleteView(BasicDeleteView):
    model = Issue
    template_name = "adminportal/proddel.html"
    context_object_name = 'delete_product'

    def get_success_url(self):
        project_slug = self.kwargs['slug']
        project_issue = Issue.objects.get(slug = project_slug)
        project = project_issue.project_name.slug
        # print("Self-----><-><-Slug", project)
        return reverse_lazy('tudu:project_detail', kwargs = {'slug':project})


#--------------------------------sort---drag and drop....!!-----------------------------#

class SortByOrder(View):

    def post(self, request, *args, **kwargs):
        task_order = request.POST.getlist('item')
        issue_order = request.POST.getlist('issue')

        print("task----isuee./------order---->>", task_order, " --------Order--issue-----", issue_order)

        if task_order:
            for  idx, task in enumerate(task_order, start=1):
                user_task = Project.objects.get(pk= task)
                user_task.order = idx
                user_task.save()
            return JsonResponse({"status": "Done"})
                # print("user-tasks------------>>>", idx)
                # tasks.append(user_task)
            # print("taskkkkkkkkkkkkkkkkkkkkkkkkkkkk>>>>>", tasks)
            # return render(request, 'adminportal/partial/task_list.html', {'items': tasks})
        elif issue_order:
            for  idx, task in enumerate(issue_order, start=1):
                user_task = Issue.objects.get(pk=task)
                user_task.order = idx
                user_task.save()
            return JsonResponse({"status": "Done"})
                # print("user-tasks------------>>>", idx)
                # tasks.append(user_task)
            # print("taskkkkkkkkkkkkkkkkkkkkkkkkkkkk>>>>>", tasks)
            # return redirect('/')
            # return render(request, 'adminportal/partial/task_list.html', {'tasks': tasks})

    

#--------------------------------Report Generation..!!-----------------------------#

def over_estimated_tasks(request):
    buf = io.BytesIO()
    can = canvas.Canvas(buf, pagesize=(800,800),pageCompression=0, bottomup = 0)
    textob = can.beginText()
    textob.setTextOrigin(inch, inch)

    issue_vars = Issue.objects.all()
    lines = list()
    lines.append("-------------------Over-Estimated-Tasks--------------------")
    for issue_var in issue_vars:
        current_date = datetime.now().strftime("%d-%m-%Y")
        issue_end_date = issue_var.end_date.strftime("%d-%m-%Y")
        issue_start_date = issue_var.start_date.strftime("%d-%m-%Y")
        issue_updated_at = issue_var.updated_at.strftime("%d-%m-%Y")

        if (issue_var.status == "Pending") and (issue_end_date > issue_updated_at):
            
            lines.append("Project-Name: "+ str(issue_var.project_name))
            lines.append("Issue-Title: "+ str(issue_var.title))
            lines.append("Description: "+ str(issue_var.discription))
            lines.append("Assign-To: "+ str(issue_var.assign_to) + ", " + str(issue_var.assign_to.designation))
            lines.append("Issue-Type: "+ str(issue_var.issue_type))
            lines.append("Priority: "+ str(issue_var.priority))
            lines.append("Status: "+ str(issue_var.status))
            lines.append("Start/End-Date: "+ str(issue_start_date) + "/ "+ str(issue_end_date))
            lines.append("Completion-Date: "+ str(issue_updated_at))
            lines.append("Difficulty: "+ str(issue_var.difficulty))
            lines.append("===================================================================")
        else:
            print("out-side-if--------->>", issue_var.title)
    print("<<<_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Loop completed..!!!_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_->>>")

    for line in lines:

        if "Project-Name" in line:
            textob.setFont("Times-BoldItalic", 14)
            textob.textLine(line)

        elif "Over-Estimated" in line:
            textob.setFont("Courier-Bold", 18)
            textob.textLine(line)

        elif "Description" in line:
            wraped_text = "\n\t\t".join(wrap(line, 120)) 
            textob.setFont("Times-Roman", 14)
            textob.textLines(wraped_text)
            
        else:
            textob.setFont("Times-Roman", 14)
            textob.textLine(line)

    can.drawText(textob)
    can.showPage()
    can.save()
    buf.seek(0)
    current_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    return FileResponse(buf, as_attachment=False, filename=f'Over-Estimated-Tasks-{current_date}.pdf')

def under_estimated_tasks(request):
   
    buf = io.BytesIO()
    can = canvas.Canvas(buf, pagesize=(800,800)*2, bottomup = 0)
    textob = can.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    issue_vars = Issue.objects.all()
    current_date = datetime.now().strftime("%d-%m-%Y")
    print("date----------->><<", current_date)
    lines = list()
    lines.append("-------------------Under-Estimated-Tasks-------------------")
    for issue_var in issue_vars:
        issue_end_date = issue_var.end_date.strftime("%d-%m-%Y")
        issue_start_date = issue_var.start_date.strftime("%d-%m-%Y")
        issue_updated_at = issue_var.updated_at.strftime("%d-%m-%Y")
        if (issue_var.status == "Completed") and (issue_end_date < issue_updated_at):
            lines.append("Project-Name: "+ str(issue_var.project_name))
            lines.append("Issue-Title: "+ str(issue_var.title))
            lines.append("Description: "+ str(issue_var.discription))
            lines.append("Assign-To: "+ str(issue_var.assign_to) + ", " + str(issue_var.assign_to.designation))
            lines.append("Issue-Type: "+ str(issue_var.issue_type))
            lines.append("Priority: "+ str(issue_var.priority))
            lines.append("Status: "+ str(issue_var.status))
            lines.append("Start/End-Date: "+ str(issue_start_date) + "/ "+ str(issue_end_date))
            # lines.append("End-Date: "+ str(issue_var.end_date))
            lines.append("Completion-Date: "+ str(issue_updated_at))
            lines.append("Difficulty: "+ str(issue_var.difficulty))
            lines.append("===================================================================")
        else:
            print("out-side-if--------->>", issue_var.title)
    print("<<_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Loop completed..!!!_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_->>")

    for line in lines:

        if "Project-Name" in line:
            textob.setFont("Times-BoldItalic", 14)
            textob.textLine(line)

        elif "Under-Estimated" in line:
            textob.setFont("Courier-Bold", 18)
            textob.textLine(line)

        elif "Description" in line:
            wraped_text = "\n\t\t".join(wrap(line, 120)) 
            textob.setFont("Times-Roman", 14)
            textob.textLines(wraped_text)

        else:
            textob.setFont("Times-Roman", 14)
            textob.textLine(line)

    can.drawText(textob)
    can.showPage()
    can.save()
    buf.seek(0)
    current_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    return FileResponse(buf, as_attachment=False, filename='Under-Estimated-Tasks-{}.pdf'.format(current_date))

def delayed_tasks(request):
   
    buf = io.BytesIO()
    can = canvas.Canvas(buf, pagesize=(800,800), bottomup = 0)
    textob = can.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    issue_vars = Issue.objects.all()
    current_date = datetime.now().strftime("%d-%m-%Y")
    print("date----------->><<", current_date)
    lines = list()
    lines.append("-------------------Delayed-Tasks-------------------")
    for issue_var in issue_vars:
        issue_end_date = issue_var.end_date.strftime("%d-%m-%Y")
        issue_start_date = issue_var.start_date.strftime("%d-%m-%Y")
        issue_updated_at = issue_var.updated_at.strftime("%d-%m-%Y")
        if (issue_var.status == "Completed") and (issue_end_date < issue_updated_at):
            lines.append("Project-Name: "+ str(issue_var.project_name))
            lines.append("Issue-Title: "+ str(issue_var.title))
            lines.append("Description: "+ str(issue_var.discription))
            lines.append("Assign-To: "+ str(issue_var.assign_to) + ", " + str(issue_var.assign_to.designation))
            lines.append("Issue-Type: "+ str(issue_var.issue_type))
            lines.append("Priority: "+ str(issue_var.priority))
            lines.append("Status: "+ str(issue_var.status))
            lines.append("Start/End-Date: "+ str(issue_start_date) + "/ "+ str(issue_end_date))
            lines.append("Completion-Date: "+ str(issue_updated_at))
            lines.append("Difficulty: "+ str(issue_var.difficulty))
            lines.append("===================================================================")
        else:
            print("out-side-if--------->>", issue_var.title)
    print("<<_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Loop completed..!!!_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_->>")

    for line in lines:

        if "Project-Name" in line:
            textob.setFont("Times-BoldItalic", 14)
            textob.textLine(line)

        elif "Delayed" in line:
            textob.setFont("Courier-Bold", 18)
            textob.textLine(line)

        elif "Description" in line:
            wraped_text = "\n\t\t".join(wrap(line, 120)) 
            textob.setFont("Times-Roman", 14)
            textob.textLines(wraped_text)

        else:
            textob.setFont("Times-Roman", 14)
            textob.textLine(line)

    can.drawText(textob)
    can.showPage()
    can.save()
    buf.seek(0)
    current_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    return FileResponse(buf, as_attachment=False, filename='Delayed-Tasks-{}.pdf'.format(current_date))

