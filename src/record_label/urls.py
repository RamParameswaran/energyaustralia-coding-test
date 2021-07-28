from django.urls import path


from . import views

urlpatterns = [
    path("", views.RecordLabelListView, name="list_record_labels"),
]
