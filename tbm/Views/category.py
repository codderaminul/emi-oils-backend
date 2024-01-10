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


def editCategory(request,category_id):
    globalSubscribersID = []
    select_all = 'false'
    subscriber_filter = ''

    if request.method == 'POST':
        if request.POST.get('subscriber_select_status'):
            selected_id = request.POST.get('selected_id')
            unselected_id = request.POST.get('unselected_id')
            select_all = request.POST.get('select_all')

            if select_all == 'true':
                globalSubscribersID = []
                for subscriber in subscriber_filter.qs:
                    globalSubscribersID.append(subscriber.id)
                    
            if select_all == 'empty' and selected_id == '':
                select_all = 'false'
                globalSubscribersID = []

            if selected_id != '':
                SubscriberID = selected_id.split(',')
                for id in SubscriberID:
                    globalSubscribersID.append(int(id.strip()))
            globalSubscribersID = list(set(globalSubscribersID))

            if unselected_id != '':
                unselected = []
                UnselectedID = unselected_id.split(',')
                for id in UnselectedID:
                    unselected.append(int(id.strip()))
                unselected = list(set(unselected))
                for id in unselected:
                    if id in globalSubscribersID:
                        globalSubscribersID.remove(id)
            

        if request.POST.get('update_category_name'):
            category_name = request.POST.get('update_category_name')
            category = Category.objects.get(id = category_id)  
            category.name = category_name
            category.save()
            messages.success(request,"Update successfull")

            subscribers = Subscriber.objects.filter(id__in = globalSubscribersID)
            category.subscriber.clear()
            category.subscriber.add(*subscribers)
            globalSubscribersID = []
            select_all = 'false'
            # subscriber_filter = ''
        return redirect('tbm:category_list')

    category = Category.objects.get(id = category_id)   
    queryset = Subscriber.objects.filter(company__customuser = request.user)
    if globalSubscribersID == []:
        selected_category_items = category.subscriber.all() 
        for item in selected_category_items:
            globalSubscribersID.append(item.id)
    subscriber_filter = SubscriberFilter(request.GET, queryset=queryset,user = request.user)
    paginator = Paginator(subscriber_filter.qs, 10) 
    page = request.GET.get('page')

    try:
        subscribers = paginator.page(page)
    except PageNotAnInteger:
        subscribers = paginator.page(1)
    except EmptyPage:
        subscribers = paginator.page(paginator.num_pages)

    if len(globalSubscribersID) == len(subscriber_filter.qs) and len(globalSubscribersID) > 0:
        select_all = 'true'
    return render(request, 'category_edit.html',{'selected_item':globalSubscribersID,'subscribers':subscribers,'filter':subscriber_filter,'category_name':category.name,'category_id':category_id,'select_all':select_all})
    
