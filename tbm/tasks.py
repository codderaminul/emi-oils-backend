from celery import shared_task
from common.common_function import send_mail,send_message
from datetime import datetime, timedelta
from django_celery_beat.models import PeriodicTask
from django_twilio.decorators import twilio_view


@shared_task
def send_email(subject="task subject",message="task message",recipient="programmeraminul@gmail.com"):
    send_mail(subject=subject, message=message, recipient=list(recipient))

@shared_task
def send_sms(message="task message",recipient="+8801750170280"):
    send_message(message=message, recipient=recipient)

@shared_task
def delete_one_time_crontab():
    current_time = (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M')
    period_tasks = PeriodicTask.objects.filter(name__startswith='once')
    if len(period_tasks) > 0:
        for task in period_tasks:
            # Format the task's date and time
            task_datetime = datetime(
                year= int(task.crontab.year),
                month= int(task.crontab.month_of_year),
                day= int(task.crontab.day_of_month),
                hour= int(task.crontab.hour),
                minute=int(task.crontab.minute)
            ).strftime('%Y-%m-%d %H:%M')
            # # Compare the current time with the task's time
            if current_time > task_datetime:
                print("Task is scheduled for:", task.id)
                PeriodicTask.objects.filter(id=task.id).delete()






