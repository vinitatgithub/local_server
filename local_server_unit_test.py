import unittest
import json
from local_server import app, data_storage  # Adjust the import to your service file name


class FlaskServiceTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        data_storage.clear()  # Clear the data_storage list

    def test_delete_data_nonexistent(self):
        """Test DELETE request on nonexistent index."""
        self.app.post('/post',
                      headers={
                          'X-Requested-With': 'XMLHttpRequest',
                          'Authorization': 'Bearer your_token',
                          'Content-Type': 'application/json'
                      },
                      data=json.dumps({"key": "value"}))

        response = self.app.delete('/delete/999',
                                   headers={
                                       'X-Requested-With': 'XMLHttpRequest',
                                       'Authorization': 'Bearer your_token'
                                   })
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not found", str(response.data))

    def test_delete_data_on_empty_storage(self):
        """Test DELETE request when storage is empty."""
        response = self.app.delete('/delete/0',
                                   headers={
                                       'X-Requested-With': 'XMLHttpRequest',
                                       'Authorization': 'Bearer your_token'
                                   })
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not found", str(response.data))

    def test_delete_data_out_of_range(self):
        """Test DELETE request with index out of range."""
        response = self.app.delete('/delete/0',
                                   headers={
                                       'X-Requested-With': 'XMLHttpRequest',
                                       'Authorization': 'Bearer your_token'
                                   })
        self.assertEqual(response.status_code, 404)

    def test_delete_data_success(self):
        """Test successful DELETE request."""
        self.app.post('/post',
                      headers={
                          'X-Requested-With': 'XMLHttpRequest',
                          'Authorization': 'Bearer your_token',
                          'Content-Type': 'application/json'
                      },
                      data=json.dumps({"key": "value"}))

        response = self.app.delete('/delete/0',
                                   headers={
                                       'X-Requested-With': 'XMLHttpRequest',
                                       'Authorization': 'Bearer your_token'
                                   })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "Data deleted", "data": {"key": "value"}})

    def test_get_data_after_multiple_posts(self):
        """Test GET request after multiple POST requests to verify all data is returned."""
        for i in range(3):
            self.app.post('/post',
                          headers={
                              'X-Requested-With': 'XMLHttpRequest',
                              'Authorization': 'Bearer your_token',
                              'Content-Type': 'application/json'
                          },
                          data=json.dumps({"key": f"value_{i}"}))

        response = self.app.get('/get', headers={
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': 'Bearer your_token'
        })
        self.assertEqual(response.status_code, 200)
        expected_data = [{"key": f"value_{i}"} for i in range(3)]
        self.assertEqual(json.loads(response.data), {"data": expected_data})

    def test_get_data_empty(self):
        """Test GET request returns empty data initially."""
        response = self.app.get('/get', headers={
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': 'Bearer your_token'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"data": []})

    def test_get_data_with_invalid_header_value(self):
        """Test GET request with invalid header value."""
        response = self.app.get('/get', headers={
            'X-Requested-With': 'InvalidValue',
            'Authorization': 'Bearer wrong_token'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing or invalid header", str(response.data))

    def test_get_data_with_missing_headers(self):
        """Test GET request without mandatory headers."""
        response = self.app.get('/get')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing or invalid header", str(response.data))

    def test_get_data_with_no_posts(self):
        """Test GET request when no POST requests have been made."""
        response = self.app.get('/get', headers={
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': 'Bearer your_token'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"data": []})

    def test_get_data_with_query_parameters(self):
        """Test GET request with additional query parameters."""
        self.app.post('/post',
                      headers={
                          'X-Requested-With': 'XMLHttpRequest',
                          'Authorization': 'Bearer your_token',
                          'Content-Type': 'application/json'
                      },
                      data=json.dumps({"key": "value"}))

        response = self.app.get('/get?filter=value', headers={
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': 'Bearer your_token'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("value", str(response.data))  # Adjust the check based on your logic

    def test_patch_data_invalid_json(self):
        """Test PATCH request with invalid JSON data."""
        self.app.post('/post',
                      headers={
                          'X-Requested-With': 'XMLHttpRequest',
                          'Authorization': 'Bearer your_token',
                          'Content-Type': 'application/json'
                      },
                      data=json.dumps({"key": "value"}))

        response = self.app.patch('/patch/0',
                                  headers={
                                     'X-Requested-With': 'XMLHttpRequest',
                                     'Authorization': 'Bearer your_token',
                                     'Content-Type': 'application/json'
                                  },
                                  data='{"key": "value"')  # Malformed JSON (missing closing brace)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid JSON", str(response.data))

    def test_patch_data_nonexistent(self):
        """Test PATCH request on nonexistent index."""
        response = self.app.patch('/patch/999',
                                  headers={
                                      'X-Requested-With': 'XMLHttpRequest',
                                      'Authorization': 'Bearer your_token',
                                      'Content-Type': 'application/json'
                                  },
                                  data=json.dumps({"key": "updated_value"}))
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not found", str(response.data))

    def test_patch_data_out_of_range(self):
        """Test PATCH request with index out of range."""
        response = self.app.patch('/patch/0',
                                  headers={
                                      'X-Requested-With': 'XMLHttpRequest',
                                      'Authorization': 'Bearer your_token',
                                      'Content-Type': 'application/json'
                                  },
                                  data=json.dumps({"key": "updated_value"}))
        self.assertEqual(response.status_code, 404)

    def test_patch_data_success(self):
        """Test successful PATCH request."""
        self.app.post('/post',
                      headers={
                          'X-Requested-With': 'XMLHttpRequest',
                          'Authorization': 'Bearer your_token',
                          'Content-Type': 'application/json'
                      },
                      data=json.dumps({"key": "value"}))

        response = self.app.patch('/patch/0',
                                  headers={
                                      'X-Requested-With': 'XMLHttpRequest',
                                      'Authorization': 'Bearer your_token',
                                      'Content-Type': 'application/json'
                                  },
                                  data=json.dumps({"key": "updated_value"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data),
                         {"message": "Data patched/partially updated", "data": {"key": "updated_value"}})

    def test_post_data_duplicate(self):
        """Test posting duplicate data."""
        self.app.post('/post',
                      headers={
                          'X-Requested-With': 'XMLHttpRequest',
                          'Authorization': 'Bearer your_token',
                          'Content-Type': 'application/json'
                      },
                      data=json.dumps({"key": "duplicate_value"}))

        response = self.app.post('/post',
                                 headers={
                                     'X-Requested-With': 'XMLHttpRequest',
                                     'Authorization': 'Bearer your_token',
                                     'Content-Type': 'application/json'
                                 },
                                 data=json.dumps({"key": "duplicate_value"}))
        self.assertEqual(response.status_code, 201)

    def test_post_data_invalid_json(self):
        """Test POST request with invalid JSON data."""
        response = self.app.post('/post',
                                 headers={
                                     'X-Requested-With': 'XMLHttpRequest',
                                     'Authorization': 'Bearer your_token',
                                     'Content-Type': 'application/json'
                                 },
                                 data='{"key": "value"')  # Malformed JSON (missing closing brace)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid JSON", str(response.data))

    def test_post_data_success(self):
        """Test successful POST request."""
        response = self.app.post('/post',
                                 headers={
                                     'X-Requested-With': 'XMLHttpRequest',
                                     'Authorization': 'Bearer your_token',
                                     'Content-Type': 'application/json'
                                 },
                                 data=json.dumps({"key": "value"}))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {"message": "Data received", "data": {"key": "value"}})

    def test_post_data_with_identical_values(self):
        """Test multiple POST requests with identical values."""
        for _ in range(3):
            self.app.post('/post',
                          headers={
                              'X-Requested-With': 'XMLHttpRequest',
                              'Authorization': 'Bearer your_token',
                              'Content-Type': 'application/json'
                          },
                          data=json.dumps({"key": "identical_value"}))

        response = self.app.get('/get', headers={
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': 'Bearer your_token'
        })
        self.assertEqual(response.status_code, 200)
        expected_data = [{"key": "identical_value"}] * 3
        self.assertEqual(json.loads(response.data), {"data": expected_data})

    def test_post_data_with_invalid_content_type(self):
        """Test POST request with invalid Content-Type header."""
        response = self.app.post('/post',
                                 headers={
                                     'X-Requested-With': 'XMLHttpRequest',
                                     'Authorization': 'Bearer your_token',
                                     'Content-Type': 'text/plain'  # Invalid content type
                                 },
                                 data='{"key": "value"}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid Content-Type", str(response.data))

    def test_post_data_with_invalid_header_value(self):
        """Test POST request with invalid header values."""
        response = self.app.post('/post',
                                 headers={
                                     'X-Requested-With': 'InvalidHeaderValue',
                                     'Authorization': 'Bearer your_token',
                                     'Content-Type': 'application/json'
                                 },
                                 data=json.dumps({"key": "value"}))
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing or invalid header", str(response.data))

    def test_post_data_with_missing_authorization_header(self):
        """Test POST request with missing Authorization header."""
        response = self.app.post('/post',
                                 headers={
                                     'X-Requested-With': 'XMLHttpRequest',
                                     'Content-Type': 'application/json'
                                 },
                                 data=json.dumps({"key": "value"}))
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing or invalid header", str(response.data))

    def test_post_data_with_missing_x_requested_with_header(self):
        """Test POST request with missing X-Requested-With header."""
        response = self.app.post('/post',
                                 headers={
                                     'Authorization': 'Bearer your_token',
                                     'Content-Type': 'application/json'
                                 },
                                 data=json.dumps({"key": "value"}))
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing or invalid header", str(response.data))

    def test_post_multiple_calls(self):
        """Test multiple POST requests and ensure all data is stored correctly."""
        responses = []
        for i in range(5):
            response = self.app.post('/post',
                                     headers={
                                         'X-Requested-With': 'XMLHttpRequest',
                                         'Authorization': 'Bearer your_token',
                                         'Content-Type': 'application/json'
                                     },
                                     data=json.dumps({"key": f"value_{i}"}))
            responses.append(response)

        for response in responses:
            self.assertEqual(response.status_code, 201)

        get_response = self.app.get('/get', headers={
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': 'Bearer your_token'
        })
        self.assertEqual(get_response.status_code, 200)
        expected_data = [{"key": f"value_{i}"} for i in range(5)]
        self.assertEqual(json.loads(get_response.data), {"data": expected_data})

    def test_put_data_invalid_json(self):
        """Test PUT request with invalid JSON data."""
        self.app.post('/post',
                      headers={
                          'X-Requested-With': 'XMLHttpRequest',
                          'Authorization': 'Bearer your_token',
                          'Content-Type': 'application/json'
                      },
                      data=json.dumps({"key": "value"}))

        response = self.app.put('/put/0',
                                headers={
                                    'X-Requested-With': 'XMLHttpRequest',
                                    'Authorization': 'Bearer your_token',
                                    'Content-Type': 'application/json'
                                },
                                data='{"key": "value"')  # Malformed JSON (missing closing brace)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid JSON", str(response.data))

    def test_put_data_nonexistent(self):
        """Test PUT request on nonexistent index."""
        response = self.app.put('/put/999',
                                headers={
                                    'X-Requested-With': 'XMLHttpRequest',
                                    'Authorization': 'Bearer your_token',
                                    'Content-Type': 'application/json'
                                },
                                data=json.dumps({"key": "new_value"}))
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not found", str(response.data))

    def test_put_data_out_of_range(self):
        """Test PUT request with index out of range."""
        response = self.app.put('/put/0',
                                headers={
                                    'X-Requested-With': 'XMLHttpRequest',
                                    'Authorization': 'Bearer your_token',
                                    'Content-Type': 'application/json'
                                },
                                data=json.dumps({"key": "new_value"}))
        self.assertEqual(response.status_code, 404)

    def test_put_data_success(self):
        """Test successful PUT request."""
        self.app.post('/post',
                      headers={
                          'X-Requested-With': 'XMLHttpRequest',
                          'Authorization': 'Bearer your_token',
                          'Content-Type': 'application/json'
                      },
                      data=json.dumps({"key": "value"}))

        response = self.app.put('/put/0',
                                headers={
                                    'X-Requested-With': 'XMLHttpRequest',
                                    'Authorization': 'Bearer your_token',
                                    'Content-Type': 'application/json'
                                },
                                data=json.dumps({"key": "new_value"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "Data updated", "data": {"key": "new_value"}})


if __name__ == '__main__':
    unittest.main()
