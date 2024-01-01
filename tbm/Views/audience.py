from django.forms.models import model_to_dict
from django.contrib import messages
from django.shortcuts import redirect, render
from account.models import Category, Company, Subscriber
from django.http import JsonResponse
import django_filters
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_category(request,category_id):
    if category_id == 'select_all':
        subscribers = Subscriber.objects.filter(company__customuser=request.user)
    else:
        category = Category.objects.get(id=int(category_id)) 
        subscribers = category.subscriber.all()
    subscriber_list = []
    company_list = []
    if len(subscribers) > 0:
        for subscriber in subscribers:
            formatted_date = subscriber.created_at.strftime('%Y-%m-%d')
            company_data = model_to_dict(subscriber.company) 
            subscriber_data = {
                'id': subscriber.id,
                'first_name': subscriber.first_name,
                'last_name': subscriber.last_name,
                'email': subscriber.email,
                'phone': subscriber.phone,
                'whatsapp': subscriber.whatsapp,
                'company': company_data,
                'age': subscriber.age,
                'gender': subscriber.gender,
                'country': subscriber.country,
                'created_at': formatted_date,
            }
            subscriber_list.append(subscriber_data)
            companies = request.user.company.all()
            for company in companies:
                company_data = {
                    'id':company.id,
                    'name':company.name,
                }
                company_list.append(company_data)
    else:
        subscriber_list = []
    return JsonResponse({'subscriber_list': subscriber_list,'companies':company_list}, status=200)

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
            
@login_required(login_url='/')  # Specify the login URL        
def audience(request):
    if request.method == 'POST':
        if request.POST.get('first_name'):
            id = request.POST.get('subscribe_id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            whatsapp = request.POST.get('whatsapp')
            country = request.POST.get('country')
            age = request.POST.get('age')
            company = request.POST.get('company')
            gender = request.POST.get('gender')

            companies = request.user.company.all()
            company_id = None
            for mycompany in companies:
                if mycompany.name == company:
                    company_id = mycompany.id

            if company_id is not None:
                Subscriber.objects.filter(id=id).update(first_name=first_name,last_name=last_name,email=email,phone=phone,whatsapp=str(whatsapp),age=age,country=country,gender=gender,company=Company.objects.get(id=company_id))
            else:
                 Subscriber.objects.filter(id=id).update(first_name=first_name,last_name=last_name,email=email,phone=phone,whatsapp=str(whatsapp),age=age,country=country,gender=gender)
            return JsonResponse({'status': 'ok'})

        if request.POST.get('delete_subscribe_id'):
            delete_id = request.POST.get('delete_subscribe_id')
            Subscriber.objects.filter(id=delete_id).delete()
            return JsonResponse({'status': 'ok'})
    
        if 'create_category' in request.POST:
            try:
                c_name = request.POST.get('create_category_name', False)
                if Category.objects.filter(user=request.user,name=c_name).exists():
                    messages.error(request,"Already Exists This Name")
                    return redirect('tbm:subscribers') 
                # Get selected subscriber IDs from the hidden input
                selected_subscriber_ids = request.POST.get('create_category_subscriber_id_list', '').split(',')
                selected_subscribers = Subscriber.objects.filter(id__in=selected_subscriber_ids)
                new_cat = Category.objects.create(user=request.user, name=c_name)
                messages.success(request,'Create category successful')
                # Retrieve Subscriber instances based on the selected IDs
                # Add all selected subscribers to the new category
                new_cat.subscriber.add(*selected_subscribers)
            except:
                messages.error(request,'Please select first')

    queryset = Subscriber.objects.filter(company__customuser = request.user)
    subscriber_filter = SubscriberFilter(request.GET, queryset=queryset,user=request.user)
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
    categories = Category.objects.filter(user = request.user)
    
    return render(request, 'audience.html', {'filter': subscriber_filter,'subscribers': subscribers})
