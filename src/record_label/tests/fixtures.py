import json

festivals_api_response = json.dumps(
    [
        {
            "label": "Record Label 1",
            "bands": [{"name": "Band X", "festivals": [{"name": "Omega Festival"}]}],
        },
        {
            "label": "Record Label 2",
            "bands": [
                {
                    "name": "Band A",
                    "festivals": [
                        {"name": "Alpha Festival"},
                        {"name": "Beta Festival"},
                    ],
                }
            ],
        },
    ]
)
