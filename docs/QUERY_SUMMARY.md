# OpenSearch Query Summary

Your task is to generate a Python script that queries Opensearch

This document summarizes the OpenSearch indices and their available attributes (fields) identified from the codebase examples. Use this reference to construct queries for the OpenSearch backend.

**Note:** Only indices matching `ai-research-shell-*` are relevant for this context.

## Common Patterns
- **Dates**: Most indices use `date` (format: YYYY-MM-DD).
- **Items**: Queried by `item` (string).
- **Errors**: Many queries explicitly exclude documents where the `error` field exists:
  ```json
  "must_not": [{"exists": {"field": "error"}}]
  ```
- **Environment**: The standard environment prefix is `ai-research-shell-`.

## Index Definitions

### 1. Item Status & Master Data
**Index**: `ai-research-shell-item-3`
*   **Attributes**: `item`, `date`, `error`, `latestBomLevel`, `childrenCount`, `criticalStockDays`, `evaluation`, `pendingDemand`, `anticipation`, `anticipationBias`.

### 2. Bill of Materials (BOM)
**Index**: `ai-research-shell-bom-3`
*   **Attributes**: `item`, `date`, `location`, `onHandQuantityValue`, `latestBomLevel`, `belowDistinctCount`, `asrLeadTime`, `supplyArchiveCount`, `rule`.

### 3. Inference & Planning Results
**Index**: `ai-research-shell-inference-3`
*   **Attributes**: `item`, `date`, `forwardPlan` (Nested Object), `averageOnHandQuantityFuture`, `isRTO`, `criticalStockValueIncludingAggressiveTotal`, `anticipation`, `minimumOrderQuantity`.
*   **Nested `forwardPlan` fields**: `date`, `supplyDue`, `onHandQuantity`, `topOfOrange`, `latestBomLevel`.

### 4. Planning Board
**Index**: `ai-research-shell-planning-board`
*   **Attributes**: `item`, `date`, `gaugePriotity`, `gauge`, `orderQuantity`, `latestBomLevel`.

### 5. Snapshot / Metrics
**Index**: `ai-research-shell-snap-3`
*   **Attributes**: `item`, `date`, `snapRatio`, `latestBomLevel`, `criticalStockDays`, `planningBoardHasReorderCall`, `success`.

### 6. Archives (Historical Data)
**Indices**:
*   `ai-research-shell-archive-bom`
*   `ai-research-shell-archive-closed-demand`
*   `ai-research-shell-archive-current-demand`
*   `ai-research-shell-archive-current-onhand`
*   `ai-research-shell-archive-current-supply`
*   `ai-research-shell-archive-demand`
*   `ai-research-shell-archive-forecast`
*   `ai-research-shell-archive-onhand`
*   `ai-research-shell-archive-part-master`
*   `ai-research-shell-archive-supply`
*   `ai-research-shell-archive-v6-planning-board`

## Available Python Script Examples

**IMPORTANT:** Your task is to generate a Python script that queries Opensearch. All code examples below are fully functional, standalone Python scripts that can be copied and executed directly without any modifications. They include all necessary imports and are ready to run as complete programs.

Below are examples of how to query these indices using the project's `utils.readopense` module.

### Multi-Variable Aggregations: Value by Location
**Script**: `ai_research_aggs_per_location_and_value.py`
**Goal**: Group data by one variable (`location`) and calculate a metric (`sum`) on a second variable (`onHandQuantityValue`).
**Index**: `ai-research-shell-inference-3`
```python
import logging
import json
from utils.readopense import readopense
from datetime import date

logging.getLogger().setLevel("INFO")

today_str = date.today().strftime("%Y-%m-%d")

payload = {
    "payload": {
        "size": 0,
        "query": {
            "bool": {
                "must": [{"match": {"date": today_str}}],
                "must_not": [{"exists": {"field": "error"}}],
            }
        },
        "aggs": {
            "by_location": {
                "terms": {
                    "field": "location",
                    "size": 1000,
                    "order": {"_count": "desc"},
                },
                "aggs": {
                    "total_value": {
                        "sum": {"field": "onHandQuantityValue"}
                    }
                },
            }
        },
    },
    "index": "ai-research-shell-inference-3",
}
```

### Inference Analysis: Nested Query for Forward Plan
**Script**: `ai_research_inference_analysis.py`
**Index**: `ai-research-shell-inference-3`
**Goal**: Find items with `supplyDue > 1,000,000` in a specific date range.
```python
import logging
import json
from utils.readopense import readopense

logging.getLogger().setLevel("INFO")

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

payload = {
    "payload": {
        "size": 100,
        "query": {
            "bool": {
                "must": [
                    {
                        "nested": {
                            "path": "forwardPlan",
                            "query": {
                                "bool": {
                                    "must": [
                                        {
                                            "range": {
                                                "forwardPlan.date": {
                                                    "gte": START_DATE,
                                                    "lte": END_DATE,
                                                }
                                            }
                                        },
                                        {"range": {"forwardPlan.supplyDue": {"gt": 1000000}}},
                                    ]
                                }
                            },
                        }
                    },
                ],
                "must_not": [{"exists": {"field": "error"}}],
            }
        },
        "_source": {
            "includes": [
                "date", "item", "forwardPlan", "latestBomLevel",
                "averageOnHandQuantityFuture", "isRTO"
            ]
        },
        "sort": [{"date": {"order": "desc"}}],
    },
    "index": "ai-research-shell-inference-3",
}
```

### Complex Analysis & Reporting (Post-Processing)
**Script**: `ai_research_inference_analysis_2.py`
**Goal**: Query raw data, calculate derived metrics (Supply/Inventory Ratio), sort, and print a formatted table.

**Note**: The `tabulate` library is available in the environment for generating professional-looking tables easily.

```python
import logging
import json
from utils.readopense import readopense
from tabulate import tabulate

logging.getLogger().setLevel("INFO")

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

# Query: Fetch items with supply due in a date range
payload = {
    "payload": {
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    {
                        "nested": {
                            "path": "forwardPlan",
                            "query": {
                                "bool": {
                                    "must": [
                                        {
                                            "range": {
                                                "forwardPlan.date": {
                                                    "gte": START_DATE,
                                                    "lte": END_DATE,
                                                }
                                            }
                                        },
                                        {"range": {"forwardPlan.supplyDue": {"gt": 0}}},
                                    ]
                                }
                            },
                        }
                    },
                ],
                "must_not": [{"exists": {"field": "error"}}],
            }
        },
        "_source": {
            "includes": [
                "date", "item", "forwardPlan", "averageOnHandQuantityFuture"
            ]
        },
        "sort": [{"date": {"order": "desc"}}],
    },
    "index": "ai-research-shell-inference-3",
}

response = readopense(payload)

# Processing: Calculate ratios
supply_ratio_data = []
for hit in response:
    item = hit['_source']['item']
    date = hit['_source']['date']
    avg_on_hand = hit['_source']['averageOnHandQuantityFuture']
    for plan in hit['_source']['forwardPlan']:
        supply_due = plan['supplyDue']
        ratio = supply_due / avg_on_hand if avg_on_hand != 0 else float('inf')
        supply_ratio_data.append({
            'item': item,
            'date': date,
            'supplyDue': supply_due,
            'ratio': ratio
        })

# Sorting: Sort by ratio descending
supply_ratio_data.sort(key=lambda x: x['ratio'], reverse=True)

# Prepare data for tabulate
table_data = []
for entry in supply_ratio_data[:10]:  # Show top 10
    ratio_display = f"{entry['ratio']:.2f}" if entry['ratio'] != float('inf') else "∞"
    table_data.append([
        entry['item'],
        entry['date'],
        f"{entry['supplyDue']:,.0f}",
        ratio_display
    ])

# Display using tabulate
print(tabulate(table_data, headers=['Item', 'Date', 'SupplyDue', 'Ratio'], tablefmt='grid'))
```

### Data Extraction for Plotting: Anticipation vs Critical Value
**Script**: `ai_research_inference_anticipation_vs_critical_value.py`
**Index**: `ai-research-shell-inference-3`
```python
import logging
import json
from utils.readopense import readopense
from datetime import date

logging.getLogger().setLevel("INFO")

today_str = date.today().strftime("%Y-%m-%d")

payload = {
    "payload": {
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    {"match": {"date": today_str}},
                    {"range": {"criticalStockValueIncludingAggressiveTotal": {"gt": 0}}},
                    {"match": {"isRTO": False}},
                ],
                "must_not": [{"exists": {"field": "error"}}],
            }
        },
        "_source": {
            "includes": [
                "item", "date", "anticipation",
                "criticalStockValueIncludingAggressiveTotal",
            ]
        },
        "sort": [{"criticalStockValueIncludingAggressiveTotal": {"order": "desc"}}],
    },
    "index": "ai-research-shell-inference-3",
}
```

### Basic Item Lookup
**Script**: `ai_research_item.py`
**Index**: `ai-research-shell-item-3`
```python
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
                     # {"match": {"item": "550051194 Z296"}},
                ],
                "must_not": [{"exists": {"field": "error"}}],
            }
        },
    },
    "index": "ai-research-shell-item-3",
}
```

### Snapshot Metrics
**Script**: `ai_research_snap.py`
**Index**: `ai-research-shell-snap-3`
```python
payload = {
    "payload": {
        "size": 10,
        "query": {
            "bool": {
                "must": [
                    {"match": {"date": "2025-08-01"}},
                    {
                        "range": {
                            "snapRatio": {
                                "lt": 1.0,
                                "gt": 0.2
                            }
                        }
                    },
                ],
                "must_not": [{"exists": {"field": "error"}}],
            }
        },
        "_source": {
            "includes": ["item", "snapRatio", "latestBomLevel"],
        },
        "sort": [{"snapRatio": {"order": "asc"}}],
    },
    "index": "ai-research-shell-snap-3",
}
```

### Planning Board Priorities
**Script**: `ai_research_planing_board.py`
**Index**: `ai-research-shell-planning-board`
```python
payload = {
    "payload": {
        "size": 10,
        "query": {
            "bool": {
                "must": [
                    {"match": {"date": "2025-12-05"}},
                    {"match": {"gaugePriotity": -2}},
                    {"range": {"orderQuantity": {"gte": 0}}},
                ]
            }
        },
        "sort": [{"date": {"order": "desc"}}],
    },
    "index": "ai-research-shell-planning-board",
}
```

### Distinct Values (Unique Lists)
**Script**: `readopense_distinct_locations.py`
**Goal**: Get a unique list of all values for a specific attribute (e.g., `location` or `partTypeCode`).
```python
import logging
import json
from utils.readopense import readopense

logging.getLogger().setLevel("INFO")

payload = {
    "payload": {
        "size": 0,  # Only aggregations
        "aggs": {
            "distinct_values": {
                "terms": {
                    "field": "location", 
                    "size": 10000
                }
            }
        },
        "query": {
            "bool": {
                "must": [{"term": {"date": "2025-07-21"}}],
                "must_not": [{"exists": {"field": "error"}}]
            }
        }
    },
    "index": "ai-research-shell-inference-3",
}

response = readopense(payload)

# Extract unique values
distinct_locations = [bucket['key'] for bucket in response['aggregations']['distinct_values']['buckets']]
print(json.dumps(distinct_locations, indent=2))
```

### Archive Examples
The following patterns are used for various archive indices:

**Script**: `ai_research_archive_current_demand.py`
**Index**: `ai-research-shell-archive-current-demand`
```python
payload = {
    "payload": {
        "size": 10,
        "query": {
            "bool": {
                "must": [
                    {"match": {"orderNumber": "Not Known"}}
                ]
            }
        },
    },
    "index": "ai-research-shell-archive-current-demand"
}
```

**Script**: `ai_research_archive_supply.py`
**Index**: `ai-research-shell-archive-supply`
```python
payload = {
    "payload": {
        "size": 1,
        "query": {
            "bool": {
                "must": [
                    {"match": {"date": "2025-11-24"}},
                ]
            }
        },
    },
    "index": "ai-research-shell-archive-supply",
}
```
