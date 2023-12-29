from django.urls import path
from core.views import save_email,CsvUpload

app_name = 'core'

urlpatterns = [
    path("save-email/",save_email,name="save_email"),
    path("upload-csv-file/",CsvUpload.as_view(),name="upload_csv"),
]
