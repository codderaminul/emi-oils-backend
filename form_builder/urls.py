from django.urls import path,include
from form_builder.views import FormBuilder,form_page

app_name = 'form_builder'

urlpatterns = [
    path('', FormBuilder.as_view(),name='builder_page'),
    path('<str:page_name>/', form_page,name='form_page'),

]