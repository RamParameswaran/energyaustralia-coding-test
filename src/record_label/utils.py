from record_label.models import Band, BandLabel, MusicFestival, RecordLabel

from record_label.serializers import RecordLabelSerializer


def restructure_data(festivals_api_data):
    """A helper function to restructure the data from the festivals API
    into the RecordLabel structure output by our API.

    :args:
    - `festivals_api_data`: a list of Python objects

    :returns:
    - `record_labels`: a list of Python objects with the following schema:
        [
            {"label": <str>,
             "bands": [
                        {"name": <str>,
                         "festivals: [{"name": <str>},]
                        }
                      ]
            },
        ]
    """

    for festival in festivals_api_data:
        # Create MusicFestival object in ORM
        festival_obj, _ = MusicFestival.objects.get_or_create(name=festival.get("name"))

        bands = festival.get("bands", [])

        for band in bands:
            band_obj, _ = Band.objects.get_or_create(name=band.get("name"))
            label_obj, _ = RecordLabel.objects.get_or_create(
                name=band.get("recordLabel")
            )

            bandlabel_obj, _ = BandLabel.objects.get_or_create(
                band=band_obj, recordLabel=label_obj
            )
            festival_obj.bands.add(bandlabel_obj)

    out = RecordLabelSerializer(RecordLabel.objects.all(), many=True).data

    # Cleanup DB
    MusicFestival.objects.all().delete()
    BandLabel.objects.all().delete()
    Band.objects.all().delete()
    RecordLabel.objects.all().delete()

    return out
