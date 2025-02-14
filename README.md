# Analytics Labs API

A step-by-step guide.

## Step 1: Installation

Install the required dependency:

```bash
pip install requests
```

## Step 2: Initialize the Client

First, import the necessary classes and create an API client instance:

```python
from analytics_labs_api import AnalyticsLabsAPI, Filter

api = AnalyticsLabsAPI(
    base_url="YOUR_API_BASE_URL",  # Replace with your API base URL
    api_key="YOUR_API_KEY"         # Replace with your API key
)
```

## Step 3: Explore Your Dataset

Before making data requests, it's helpful to understand what data is available. Use the describe_dataset method:

```python
# Get dataset description
description = api.describe_dataset(
    account_id="YOUR_ACCOUNT_ID",
    dataset_id="YOUR_DATASET_ID"
)

# The description contains available fields, measures, and metadata
print(description)
```

## Step 4: Make Data Requests

### Basic Request

Start with a simple request to get data:

```python
response = api.get_data(
    account_id="YOUR_ACCOUNT_ID",
    dataset_id="YOUR_DATASET_ID"
)
```

### Request with Specific Fields and Measures

Select particular fields and measures:

```python
response = api.get_data(
    account_id="YOUR_ACCOUNT_ID",
    dataset_id="YOUR_DATASET_ID",
    fields=["'Date (Action)'[Year Name]", "'Account'[Account Name]"],
    measures=["Actual - Spend - Gross"]
)
```

### Request with Filters

Add filters to your request:

```python
# Create a filter
filters = [
    Filter(
        field="'Date (Action)'[Year Name]",
        operator="equals",
        value=2024
    )
]

# Make request with filter
response = api.get_data(
    account_id="YOUR_ACCOUNT_ID",
    dataset_id="YOUR_DATASET_ID",
    fields=["'Date (Action)'[Year Name]", "'Account'[Account Name]"],
    measures=["Actual - Spend - Gross"],
    filters=filters
)
```

## Step 5: Understanding Response Formats

The API supports three response formats which you can specify using the `format` parameter:

### Row Format (default)

```python
response = api.get_data(
    account_id="YOUR_ACCOUNT_ID",
    dataset_id="YOUR_DATASET_ID",
    format="row"
)

# Response structure:
# {
#   "payload": [
#     {
#       "COLUMN_NAME_1": "value1",
#       "COLUMN_NAME_2": "value2"
#     }
#   ]
# }
```

### Column Format

```python
response = api.get_data(
    account_id="YOUR_ACCOUNT_ID",
    dataset_id="YOUR_DATASET_ID",
    format="column"
)

# Response structure:
# {
#   "payload": [
#     {
#       "header": "COLUMN_NAME_A",
#       "values": ["value1", "value2", "value3"]
#     }
#   ]
# }
```

### Array Format

```python
response = api.get_data(
    account_id="YOUR_ACCOUNT_ID",
    dataset_id="YOUR_DATASET_ID",
    format="array"
)

# Response structure:
# {
#   "payload": {
#     "headers": ["COLUMN_1", "COLUMN_2"],
#     "values": [
#       ["row1_col1", "row1_col2"],
#       ["row2_col1", "row2_col2"]
#     ]
#   }
# }
```

## Best Practices

1. Always use the preview parameter first for large datasets:

```python
# Check row count
preview = api.get_data(
    account_id="YOUR_ACCOUNT_ID",
    dataset_id="YOUR_DATASET_ID",
    preview=True
)
```

2. Use exact field names from describe_dataset
3. Don't modify field locators (e.g., "'Date (Action)'[Year Name]")
4. Field names are case-sensitive and must be an exact match. 

## Need Help?

Contact Analytics Labs support at support@aldc.io
