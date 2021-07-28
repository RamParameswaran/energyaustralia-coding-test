from django.db import models


class RecordLabel(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)


class Band(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)


class BandLabel(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="bandlabels")
    recordLabel = models.ForeignKey(
        RecordLabel,
        on_delete=models.CASCADE,
    )


class MusicFestival(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    bands = models.ManyToManyField(BandLabel)
