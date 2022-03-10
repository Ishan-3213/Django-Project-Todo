from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'tudu'

urlpatterns = [

    path("", HomeView.as_view(), name="index"),
    path("sorry-not-allowed/", NoPermissionView.as_view(), name="no_permission"),
    path("search/", SearchView.as_view(), name="search"),
    path('sort/', SortByOrder.as_view(), name='sort'),

    path('add-project/', ProjectCreateView.as_view(), name='project'),
    path('project-detail/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('update-project/<slug:slug>', ProjectUpdateView.as_view(), name='project_update'),
    path('delete-project/<slug:slug>', ProjectDeleteView.as_view(), name='project_delete'),

    path("issue/", IssueListView.as_view(), name="issue_list"),
    path('project/<slug:slug>', IssueCreateView.as_view(), name='issue'),
    path('project/update-issue/<slug:slug>', IssueUpdateView.as_view(), name='issue_update'),
    path('project/delete-issue/<slug:slug>', IssueDeleteView.as_view(), name='issue_delete'),
    path('project/<slug:slug>/<int:pk>', IssueDetailView.as_view(), name='issue_detail'),

    path('users/', UserListView.as_view(), name='users'),
    path('update-users/<int:pk>', UserUpdateView.as_view(), name='user_update'),
    path('delete-users/<int:pk>', UserDeleteView.as_view(), name='user_delete'),
    path('user/<int:pk>', UserDetailView.as_view(), name='user_detail'),

    path('registration/', AdminRegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(template_name='adminportal/login.html'), name='login'),
    path('logged-out/', LogoutView.as_view(template_name='adminportal/login.html'), name='logout'),

    path('over-estimated-tasks/', views.over_estimated_tasks, name='over_estimated_tasks'),
    path('under-estimated-tasks/', views.under_estimated_tasks, name='under_estimated_tasks'),
    path('delayed-tasks/', views.delayed_tasks, name='delayed_tasks'),
    
]