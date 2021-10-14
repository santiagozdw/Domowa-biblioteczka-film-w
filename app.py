from os import abort
from flask import Flask, json, jsonify, abort
from flask.globals import request
from flask.helpers import make_response
from models import items
app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.route('/git ', methods=['GET'])
def get_all():
    return jsonify(items.all())

@app.route('/api/v1/items/<int:item_id>', methods=['GET'])
def get_one(item_id):
    return jsonify(items.get(item_id))

@app.route('/api/v1/items', methods=['POST'])
def add_item():
    if not request.json or not 'title' in request.json or not 'year' in request.json or not 'type' in request.json:
        abort(400)
    item = {
        "id": items.all()[-1]['id'] + 1,
        "title": request.json.title,
		"year": request.json.year,
		"type": request.json.type,
		"views": 0
    }    
    items.all(item)
    return jsonify(item)
@app.route('/api/v1/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    success = items.delete(item_id)
    if not success:
        abort(404)
    return jsonify({'success': success})

@app.route('/api/v1/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = items.get(item_id)
    if not item:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'year' in data and not isinstance(data.get('year'), int),
        'type' in data and not isinstance(data.get('type'), str),
        'vievs' in data and not isinstance(data.get('title'), int),
    ]):
        abort(400)

    item = {
        'id': data.get('id', item['id']),
        'title': data.get('title', item['title']),
        'year': data.get('year', item['year']),
        'type': data.get('type', item['type']),
        'views': data.get('views', item['views'])
    }
    items.update(item_id, item)
    return jsonify(item)