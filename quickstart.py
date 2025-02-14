import requests
import json


class AnalyticsLabsAPI:
    def __init__(self, base_url, api_key):
        """Initialize the Analytics Labs API client.

        Args:
            base_url: Base URL for the API
            api_key: Your API key for authentication
        """
        self.base_url = base_url
        self.headers = {"Authorization": api_key, "Content-Type": "application/json"}

    def get_data(
        self,
        account_id,
        dataset_id,
        fields=None,
        measures=None,
        filters=None,
        format="row",
        preview=False,
    ):
        """Fetch data from the Analytics Labs API.

        Args:
            account_id: Client account ID
            dataset_id: Dataset identifier
            fields: Optional list of fields to retrieve. These should be the "column_locator"
                   values from the describe_dataset response's columns array
            measures: Optional list of measures to retrieve, found as "measure_name" in describe_dataset
            filters: Optional list of filter dictionaries with keys: field, operator, value.
                    The field should be a "column_locator" value from describe_dataset
            format: Response format ("row", "column", or "array")
            preview: If True, returns only row count

        """
        url = f"{self.base_url}/v1/dataset/request"

        formatted_filters = []
        if filters:
            formatted_filters = [
                {"field": f["field"], "operator": f["operator"], "value": f["value"]}
                for f in filters
            ]

        payload = {
            "account_id": account_id,
            "dataset_id": dataset_id,
            "preview": preview,
            "request": {
                "format": format,
                "fields": fields or [],
                "measures": measures or [],
                "filters": formatted_filters,
            },
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def describe_dataset(self, account_id, dataset_id):
        """Get detailed information about a dataset.

        Args:
            account_id: Client Account ID
            dataset_id: Dataset identifier

        Note: Use the "column_locator" values from the response's columns array
        when specifying fields in get_data()
        """
        url = f"{self.base_url}/v1/dataset/describe"

        payload = {"account_id": account_id, "dataset_id": dataset_id}

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()


# Usage Examples
if __name__ == "__main__":
    # Initialize the API client
    api = AnalyticsLabsAPI(base_url="https://api-test.aldc.io", api_key="API_KEY")

    # Example 1: Get dataset description
    # This will return metadata including column_locator values needed for subsequent API calls
    response = api.describe_dataset(
        account_id="ACCOUNT_ID",
        dataset_id="DATASET_ID",
    )
    print("Example 1 - Dataset description:")
    print(json.dumps(response, indent=2))

    # # Example 2: Fetch data with filters
    filters = [
        {
            "field": "COLUMN_LOCATOR_1",  # Use column_locator from describe_dataset
            "operator": "equals",
            "value": 2025,
        }
    ]

    filtered_data = api.get_data(
        account_id="ACCOUNT_ID",
        dataset_id="DATASET_ID",
        fields=["COLUMN_LOCATOR_1", "COLUMN_LOCATOR_2", "COLUMN_LOCATOR_3"],
        measures=["MEASURE_NAME_1, MEASURE_NAME_2"],
        filters=filters,
        format="row",
    )
    print("\nExample 2 - Data with filters:")
    print(json.dumps(filtered_data, indent=2))

    # Example 3: Preview data (get row count only)
    preview_data = api.get_data(
        account_id="ACCOUNT_ID", dataset_id="DATASET_ID", preview=True
    )
    print("\nExample 3 - Preview data (row count):")
    print(json.dumps(preview_data, indent=2))
