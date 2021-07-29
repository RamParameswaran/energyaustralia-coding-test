from django.urls import path


from . import views

urlpatterns = [
    path("", views.RecordLabelListView.as_view(), name="list_record_labels"),
]
