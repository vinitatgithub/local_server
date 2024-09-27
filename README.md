# Testing the Updated Service
## Run the Service:
Make sure you run the updated Flask service:

```python test_service.py```

## Test GET Request:
You can test the GET request with the required headers using curl:

```curl -H "X-Requested-With: XMLHttpRequest" -H "Authorization: Bearer your_token" http://127.0.0.1:5000/get```

If the headers are correct, you should get a response like:

```{"data": []}```

## Test POST Request:
Similarly, for the POST request:

```curl -X POST http://127.0.0.1:5000/post \
-H "Content-Type: application/json" \
-H "X-Requested-With: XMLHttpRequest" \
-H "Authorization: Bearer your_token" \
-d '{"key": "value"}'
```
If everything is correct, you should receive:

```{"message": "Data received", "data": {"key": "value"}}```

## Handling Errors
If you try to call the endpoints without the required headers, you will get a response indicating that the required headers are missing:

```
{
    "message": "Missing or invalid header: X-Requested-With"
}
```
This setup ensures that your service enforces mandatory headers for both GET and POST requests.

# Unit tests
## How It Works
* Testing Environment: The app.test_client() method creates a test client that simulates requests to the Flask application. This means that your unit tests can directly interact with the application without needing it to be running as a standalone service.
* Isolation: Each test runs in isolation, so any changes made to the application's state (like adding data to data_storage) during one test won't affect the others. However, if you have persistent data storage (like a database), you might need to reset it between tests.
* Running Tests: You can simply run the tests using:
```python test_flask_service.py```
* Note: You do not need to start the Flask application server before running the unit tests.

## Explanation of the Test Cases
* Setup: The setUp method initializes a test client for the Flask app. This allows you to simulate requests to the app.
### DELETE
1. __test_delete_data_nonexistent__: Attempt to delete items that don't exist.
1. __test_delete_data_on_empty_storage__: Attempt to delete items when storage does not exist.
1. __test_delete_data_out_of_range__: Tests that DELETE request for out of range is properly handled.
1. __test_delete_data_success__: Tests the DELETE request to remove an item.
### GET
1. __test_get_data_after_multiple_posts__: Similar to the previous test, but specifically checks the data returned by a single GET request after making multiple POST requests.
1. __test_get_data_empty__: Checks that the GET request returns an empty list when no data has been posted.
1. __test_get_data_with_invalid_header_value__: Tests the GET request with headers that have invalid values, expecting a 400 status.
1. __test_get_data_with_missing_headers__: Tests the GET request when no headers are provided. It should return a 400 status with an appropriate error message.
1. __test_get_data_with_no_posts__: Tests the GET request when no POST requests have been made yet, ensuring the service returns an empty data list.
1. __test_get_data_with_query_parameters__: Tests the GET request with additional query parameters.
### PATCH
1. __test_patch_data_invalid_json__: Tests the PATCH request with invalid JSON.
1. __test_patch_data_nonexistent__: Tests the PATCH request to partially update a non-existing item.
1. __test_patch_data_out_of_range__: Tests that PATCH request for out of range is properly handled.
1. __test_patch_data_success__: Tests the PATCH request to partially update an existing item.
### POST
1. __test_post_data_duplicate__: Ensure the service can handle duplicate entries for the POST call.
1. __test_post_data_invalid_json__: Ensures that the POST request correctly handles invalid JSON input.
1. __test_post_data_success__: Verifies that a valid POST request adds data and returns the correct message.
1. __test_post_data_with_identical_values__: Checks if the service can handle multiple POST requests with identical values correctly, and verifies that all instances are returned by a subsequent GET request.
1. __test_post_data_with_invalid_content_type__: Ensures the POST request responds correctly when a request is made with an incorrect Content-Type.
1. __test_post_data_with_invalid_header_value__: Tests the POST request with headers that have invalid values.
1. __test_post_data_with_missing_authorization_header__: Tests that the POST request responds correctly when authorization header is missing.
1. __test_post_data_with_missing_x_requested_with_header__: Tests the the POST request responds correctly when X-Requested-With header is missing.
1. __test_post_multiple_calls__: This test sends multiple POST requests and checks if all the responses are successful. After all the POSTs, it performs a GET request to verify that all the posted data is correctly aggregated and returned.
### PUT
1. __test_put_data_invalid_json__: Tests that the PUT request with invalid JSON input is properly handled.
1. __test_put_data_nonexistent__: Tests that PUT request for non-existent data is properly handled.
1. __test_put_data_out_of_range__: Tests that PUT request for out of range is properly handled.
1. __test_put_data_success__: Tests the PUT request to update an existing item.
