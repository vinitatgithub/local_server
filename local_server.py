from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# A simple in-memory storage for POST data
data_storage = []

REQUIRED_HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'Authorization': 'Bearer your_token'
}


def check_headers(required_headers):
    for header, value in required_headers.items():
        if request.headers.get(header) != value:
            abort(400, description=f'Missing or invalid header: {header}')


@app.route('/get', methods=['GET'])
def get_data():
    check_headers(REQUIRED_HEADERS)
    return jsonify({"data": data_storage}), 200


@app.route('/post', methods=['POST'])
def post_data():
    # Check for required headers
    check_headers(REQUIRED_HEADERS)

    # Check for valid Content-Type
    if request.content_type != 'application/json':
        return jsonify({"error": "Invalid Content-Type"}), 400

    try:
        # Attempt to parse the JSON
        data = request.get_json(force=True)
        data_storage.append(data)
        return jsonify({"message": "Data received", "data": data}), 201
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400


@app.route('/put/<int:index>', methods=['PUT'])
def put_data(index):
    # Check for required headers
    check_headers(REQUIRED_HEADERS)

    if index < 0 or index >= len(data_storage):
        return jsonify({"error": "Not found"}), 404

    try:
        data = request.get_json(force=True)
        data_storage[index] = data  # Update the item at the specified index
        return jsonify({"message": "Data updated", "data": data}), 200
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400


@app.route('/patch/<int:index>', methods=['PATCH'])
def patch_data(index):
    # Check for required headers
    check_headers(REQUIRED_HEADERS)

    if index < 0 or index >= len(data_storage):
        return jsonify({"error": "Not found"}), 404

    try:
        data = request.get_json(force=True)
        # Assuming we want to update only certain fields and not replace the entire item
        data_storage[index].update(data)  # Update the item at the specified index
        return jsonify({"message": "Data patched/partially updated", "data": data_storage[index]}), 200
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400


@app.route('/delete/<int:index>', methods=['DELETE'])
def delete_data(index):
    # Check for required headers
    check_headers(REQUIRED_HEADERS)

    if index < 0 or index >= len(data_storage):
        return jsonify({"error": "Not found"}), 404

    deleted_item = data_storage.pop(index)  # Remove the item at the specified index
    return jsonify({"message": "Data deleted", "data": deleted_item}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
