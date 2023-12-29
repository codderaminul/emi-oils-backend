import json,random,string
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from account.decorators import verified_email
from django.utils.decorators import method_decorator
from common.common_function import send_message
from account.models import Category,SMSCategory, Subscriber
from django.http import JsonResponse
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from twilio.rest import Client


class SendSMS(LoginRequiredMixin,View):
    template_name = 'sms.html'

    @method_decorator(verified_email)
    def get(self,request):
        subscribers = Subscriber.objects.filter(company__customuser=request.user)
        categories = Category.objects.filter(user = request.user)
        subscriber_list = []
        for subscriber in subscribers:
            formatted_date = subscriber.created_at.strftime('%Y-%m-%d')
            subscriber_list.append([subscriber.id,subscriber.phone,formatted_date,subscriber.country])
        context = {
            'subscribers': subscriber_list,
            'categories': categories,
        }
        return render(request, self.template_name, context)
    
    @method_decorator(verified_email)
    def post(self,request):
        if 'send_sms' in request.POST:
            try:
                category_data = request.POST.get('category_data')
                moment1 = request.POST.get('moment1')
                moment2 = request.POST.get('moment2')
                weeks = request.POST.getlist('moment3')
                months = request.POST.getlist('moment4')
                subject = request.POST.get('subject')
                message = request.POST.get('message')
                time_str = request.POST.get('time')
                date_str = request.POST.get('date')
                
                subscribe_list = json.loads(category_data)
                subscribe_list = [list(set(item['phone'] for item in subscribe_list))]  

                time_parts = time_str.split(':') 
                date_parts = date_str.split('-') 
                hour = int(time_parts[0])    
                minute = int(time_parts[1]) 
                day = int(date_parts[2])  
                month = int(date_parts[1])
                year = int(date_parts[0])   
            except Exception as e:
                print('Error: ',e)

            def create_PeriodicTask(moment):
                try:
                    if moment == 'once':
                        schedule, created = CrontabSchedule.objects.get_or_create(minute = minute,hour = hour, day_of_month = day, month_of_year = month,year=year)
                    if moment == 'daily':
                        schedule, created = CrontabSchedule.objects.get_or_create(minute = minute,hour = hour, day_of_month = '*/1')
                    if moment == 'yearly':
                        schedule, created = CrontabSchedule.objects.get_or_create(minute = minute,hour = hour, day_of_month = day, month_of_year = month)

                    PeriodicTask.objects.create(
                        crontab=schedule,
                        name= moment+''.join(random.choice(string.digits + string.ascii_lowercase) for _ in range(30)),
                        task='tbm.tasks.send_sms',
                        args=json.dumps([message,subscribe_list[0]])
                    )
                except Exception as e:
                    messages.error(request, "Please fill up all field",e)
                    return redirect('tbm:index')

            if moment1 == 'now':
                try:
                    client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
                    phone_number = settings.TWILIO_DEFAULT_CALLERID
                    for phone in subscribe_list[0]:
                        call = client.messages.create(from_=phone_number,body=message,to=phone)
                    messages.success(request,"SMS sent successful")
                except:
                    pass

            if moment1 == 'once':
                create_PeriodicTask(moment1)
                messages.success(request, "SMS sent successfully")

            if moment2 == 'daily':
                create_PeriodicTask(moment2)
                messages.success(request, "SMS sent successfully") 

            if moment2 == 'yearly':
                create_PeriodicTask(moment2)
                messages.success(request, "SMS sent successfully") 

            if moment2 == 'weekly':
                try:
                    for day in weeks:
                        schedule, created = CrontabSchedule.objects.get_or_create(minute = minute,hour = hour, day_of_week = day)
                        PeriodicTask.objects.create(
                            crontab=schedule,
                            name="weekly-"+''.join(random.choice(string.digits + string.ascii_lowercase) for _ in range(30)),
                            task='tbm.tasks.send_sms',
                            args=json.dumps([message,subscribe_list[0]])
                        )
                    messages.success(request, "SMS sent successfully") 
                except Exception as e:
                    messages.error(request, "Please fill up all field",e)
                    return redirect('tbm:index')
                
            if moment2 == 'monthly':
                try:
                    for month in months:
                        schedule, created = CrontabSchedule.objects.get_or_create(minute=minute,hour=hour,day_of_month=day,month_of_year=month)
                        PeriodicTask.objects.create(
                            crontab=schedule,
                            name="monthly-"+''.join(random.choice(string.digits + string.ascii_lowercase) for _ in range(30)),
                            task='tbm.tasks.send_sms',
                            args=json.dumps([message,subscribe_list[0]])
                        )
                    messages.success(request, "SMS sent successfully") 
                except Exception as e:
                    messages.error(request, "Please fill up all field",e)
                    return redirect('tbm:index')
        return redirect('tbm:send_sms')
        

