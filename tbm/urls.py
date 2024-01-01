from django.urls import include, path
from tbm.Views.SendEmail import IndexView,edit_category
from tbm.Views.SendSMS import SendSMS
from tbm.Views.audience import get_category,audience
from tbm.Views.category import AllCategory,EditCategory,del_category


app_name = 'tbm'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('send-sms/', SendSMS.as_view(), name='send_sms'),
    path('subscribers/', audience, name='subscribers'),
    path('category-list/', AllCategory.as_view(), name='category_list'),
    path('edit-category/<int:category_id>', EditCategory.as_view(), name='category_edit'),
    path('get-category/<str:category_id>', get_category, name='get_category'),
    path('edit-category/', edit_category, name='edit_category'),
    path('del-category/', del_category, name='del_category'),
]
