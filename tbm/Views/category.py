from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from account.decorators import verified_email
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import redirect, render
from account.models import Category, Company,SMSCategory, Subscriber
import django_filters
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

class AllCategory(LoginRequiredMixin,View):
    template_name = 'category_list.html'

    @method_decorator(verified_email)
    def get(self,request):
        categories = Category.objects.filter(user = request.user)       
        return render(request, self.template_name, {'categories':categories})
    

def del_category(request):
    category_id = request.POST.get('category_id')
    Category.objects.filter(user=request.user,id=category_id).delete()
    return JsonResponse({'result':'success'},status = 200)



class SubscriberFilter(django_filters.FilterSet):
    company__name = django_filters.ModelChoiceFilter(
        queryset=Company.objects.all(),
        empty_label='Select Company',
        )

    age__lt = django_filters.NumberFilter(field_name='age', lookup_expr='lt', label='Age Less Than')
    age__gt = django_filters.NumberFilter(field_name='age', lookup_expr='gt', label='Age Greater Than')

    created_at = django_filters.DateFilter(
        field_name='created_at',
        label='Created Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    
    created_at__lt = django_filters.DateFilter(
        field_name='created_at',
        label='Created Date Before',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    
    created_at__gt = django_filters.DateFilter(
        field_name='created_at',
        label='Created Date After',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    class Meta:
        model = Subscriber
        fields = {
            'company__name': ['exact'],  # Assuming Company model has a 'name' field
            'country': ['exact'],
            'age': ['exact'],
            'subscribed_status': ['exact'],
            'created_at': ['exact'],
            'gender': ['exact'],
            # Add more fields as needed
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.user = user
            self.filters['company__name'].queryset = Company.objects.filter(customuser=user)

class EditCategory(LoginRequiredMixin,View):
    template_name = 'category_edit.html'

    @method_decorator(verified_email)
    def get(self,request,category_id):
        category = Category.objects.get(id = category_id)   
        selected_item = category.subscriber.all()   
        queryset = Subscriber.objects.filter(company__customuser = request.user)

        subscriber_filter = SubscriberFilter(request.GET, queryset=queryset,user = request.user)
        # Add pagination
        paginator = Paginator(subscriber_filter.qs, 10)  # Show 10 subscribers per page
        page = request.GET.get('page')

        try:
            subscribers = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            subscribers = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver last page of results.
            subscribers = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'selected_item':selected_item,'subscribers':subscribers,'filter':subscriber_filter,'category_name':category.name})
    
    @method_decorator(verified_email)
    def post(self,request,category_id):
        
            category_name = request.POST.get('create_category_name')
            category = Category.objects.get(id = category_id)  
            category.name = category_name
            category.save()
            messages.success(request,"Update successfull")

            

            selected_subscriber_id = request.POST.get('create_category_subscriber_id_list', '')
            if selected_subscriber_id != 'nothing':
                selected_subscriber_id = selected_subscriber_id.split(',')
                selected_subscribers = Subscriber.objects.filter(id__in=selected_subscriber_id)
                
                subscribers = Subscriber.objects.filter(category__id = category_id)
                for subscriber in subscribers:
                    if subscriber not in selected_subscribers:
                        category.subscriber.remove(subscriber)

                category.subscriber.add(*selected_subscribers)
        
            return redirect('tbm:category_list')
    
