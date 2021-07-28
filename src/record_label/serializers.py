from rest_framework import serializers

from record_label.models import BandLabel, RecordLabel


class BandSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    festivals = serializers.SerializerMethodField()

    class Meta:
        model = BandLabel
        fields = ["name", "festivals"]

    def get_festivals(self, obj):
        return [{"name": item.name} for item in obj.musicfestival_set.all()]

    def get_name(self, obj):
        return obj.band.name


class RecordLabelSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="name")
    bands = serializers.SerializerMethodField()

    class Meta:
        model = RecordLabel
        fields = ["label", "bands"]

    def get_bands(self, obj):
        qs = BandLabel.objects.filter(recordLabel=obj)

        return BandSerializer(qs, many=True).data
