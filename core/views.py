from django.http import JsonResponse
import re, csv
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from account.models import CustomUser, Subscriber,Company
from account.decorators import verified_email
from django.utils.decorators import method_decorator
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
# Create your views here.

@csrf_exempt
def save_email(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')        
        last_name = request.POST.get('last_name')        
        email = request.POST.get('email')     
        phone = request.POST.get('phone')        
        company = request.POST.get('company')        
        coupon = request.POST.get('coupon')     

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if(re.fullmatch(regex, email)):
            company = get_object_or_404(Company, name=company,coupon=coupon)
            if Subscriber.objects.filter(email=email,company=company).exists() == False and company:
                Subscriber.objects.create(email=email,phone=phone,ip=ip,company=company,first_name=first_name,last_name=last_name,subscribed_status=True)
                return JsonResponse({'response':'ok','email':email,'ip':ip}, status=200)
    return JsonResponse({'response':'Nothing here for Emi Oils'})

class CsvUpload(LoginRequiredMixin,View):
    template_name = 'upload_csv.html'

    @method_decorator(verified_email)
    def get(self,request):
        user = request.user
        companies = user.company.all()
        return render(request, self.template_name, {'companies':companies})


    @method_decorator(verified_email)
    def post(self,request):
        if 'csv' in request.FILES:
            company = request.POST.get('company')
            company = get_object_or_404(Company, name=company)
            csv_file = request.FILES['csv']
            if not csv_file.name.endswith('.csv'):
                # messages.error(request,'Please Insert CSV File')
                return JsonResponse({'status': 'error', 'message': 'Invalid File Formate'})
                
            try:
                decoded_file = csv_file.read().decode('utf-8')
                csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

                header = next(csv_data)
                # Check column names
                expected_columns = ["FirstName", "LastName", "Email", "Phone","Age","Country","Gender"]
                if header != expected_columns:
                    # messages.error(request, 'Invalid CSV file. Column names do not match expected values.')
                    return JsonResponse({'status': 'error', 'message': 'File structure not valid.'})
            
                for row in csv_data:
                    first_name = row[0]
                    last_name = row[1]
                    email = row[2]
                    phone = row[3]
                    age = row[4]
                    country = row[5]
                    gender = row[6]

                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip = x_forwarded_for.split(',')[0]
                    else:
                        ip = request.META.get('REMOTE_ADDR')

                    if(re.fullmatch(regex, email)):
                        if Subscriber.objects.filter(email=email,company=company).exists() == False:
                            Subscriber.objects.create(email=email,phone=phone,ip=ip,company=company,first_name=first_name,last_name=last_name,country=country,age=age,gender=gender)

                # messages.success(request, 'CSV file processed successfully')
                return JsonResponse({'status': 'success','message':'Uploaded'})
            except Exception as e:
                # messages.error(request, 'Please insert valid structure csv file')
                return JsonResponse({'status': 'error', 'message': 'Upload fail'})

        return JsonResponse({'status': 'error', 'message': 'No CSV file provided'})
