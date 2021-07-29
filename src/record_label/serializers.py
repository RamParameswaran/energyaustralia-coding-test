from rest_framework import serializers

from record_label.models import BandLabel, MusicFestival, RecordLabel


class FestivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicFestival
        fields = ["name"]


class BandSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="band")
    festivals = FestivalSerializer(many=True, source="musicfestival_set")

    class Meta:
        model = BandLabel
        fields = ["name", "festivals"]


class RecordLabelSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="name")
    bands = BandSerializer(many=True, source="bandlabel_set")

    class Meta:
        model = RecordLabel
        fields = ["label", "bands"]
