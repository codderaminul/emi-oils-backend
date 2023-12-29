from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from account.decorators import verified_email
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

class FormBuilder(LoginRequiredMixin,View):
    template_name = 'form-builder.html'

    @method_decorator(verified_email)
    def get(self,request):
        return render(request, self.template_name, {})


@login_required
def form_page(request,page_name):
    current_user = request.user
    company = current_user.company.first()
    return render(request,page_name,{'page_name':page_name,'company':company})