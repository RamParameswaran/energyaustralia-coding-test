from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.RecordLabelListView.as_view(), name="list_record_labels"),
]
