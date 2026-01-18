import logging
import json
from utils.readopense import readopense

logging.getLogger().setLevel("INFO")

payload = {
    "payload": {
        "size": 1,
        "query": {
            "bool": {
                "must": [
                    # {"match": {"item": "500007300 D133"}},
                ],
                "must_not": [
                    # {
                    #     "match": {
                    #         "rule": "None"
                    #     }
                    # }
                ],
            }
        },
        "_source": {
            "includes": [
                # "children",
                # "parents",
            ]
        },
        "sort": [
            # {
            #     "inventoryDate": {
            #         "order": "desc"
            #     }
            # }
        ]
    },
    "index": "ai-research-shell-bom-3",
}

response: list[dict] = readopense(payload)

print(json.dumps(response, indent=2))
print(len(response), payload["index"])
