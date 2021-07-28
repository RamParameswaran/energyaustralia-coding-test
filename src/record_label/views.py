from django.shortcuts import render
from rest_framework.generics import APIView
from rest_framework import serializers


# Create your views here.
class RecordLabelSerializer(serializers.Serializer):
    href = serializers.CharField(default="123")


class RecordLabelListView(ApiView):
    serializer_class = RecordLabelSerializer
