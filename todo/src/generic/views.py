from django.views.generic import *
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class BasicListView(LoginRequiredMixin, ListView):
    # paginate_by = 3
    pass

class BasicCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    raise_exception = True
    permission_required = 'user.designation.Admin'
    redirect_field_name = 'next' 

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name()) 

        if not self.has_permission():
            return redirect('/sorry-not-allowed/')
        return super(BasicCreateView, self).dispatch(request, *args ,**kwargs)    

class BasicDetailView(LoginRequiredMixin, DetailView):
    pass

class BasicUpdateView(LoginRequiredMixin, UpdateView):
    pass

class BasicDeleteView(LoginRequiredMixin, DeleteView):
    pass

class NoPermissionView(LoginRequiredMixin ,TemplateView):
    template_name = 'adminportal/nopermission.html'
