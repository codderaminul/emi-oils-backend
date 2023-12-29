from django.urls import include, path
from tbm.Views.SendEmail import IndexView,del_category,edit_category
from tbm.Views.SendSMS import SendSMS
from tbm.Views.audience import Audience,get_category,aud
# from tbm.views import aud

app_name = 'tbm'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('send-sms/', SendSMS.as_view(), name='send_sms'),
    # path('subscribers/', Audience.as_view(), name='subscribers'),
    path('subscribers/', aud, name='subscribers'),
    path('get-category/<str:category_id>', get_category, name='get_category'),
    path('edit-category/', edit_category, name='edit_category'),
    path('del-category/', del_category, name='del_category'),
]
