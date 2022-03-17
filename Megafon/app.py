import datetime
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

Traffic = [
    {
        'id': 1,
        'Name': 'For free',
        'Start date': u'2002-01-01',
        'End date': u'2003-01-01',
        'Minutes': 300,
        'SMS': 150,
        'Traffic': 1024
    }
]

users = [
    {
        'id': 1,
        'Balance': 0.0,
        'Add date': u'2002-01-01',
        'Age': 40,
        'City': 'Moscow',
        'last activity': datetime.datetime.now(),
        'Traffic': Traffic[0],
        'done': False
    },
]

goals = [
    {
        'id': 1,
        'Time': u'2022-01-30 15:40:11',
        'user_id': users[0],
        'Type': 'Call',
        'Spent': 5
    }
]


@app.route('/', methods=['GET'])
def get_home():
    return 'WELCOME to my server'


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})


@app.route('/users/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, users)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Страница не найдена'}), 404)


@app.route('/users/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, users)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'balance' in request.json:
        abort(400)
    if 'Add date' in request.json:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['balance'] = request.json.get('balance', task[0]['balance'])
    task[0]['Add date'] = request.json.get('Add date',
                                           task[0]['Add date'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/users/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, users)
    if len(task) == 0:
        abort(404)
    users.remove(task[0])
    return jsonify({'result': True})


@app.route('/users', methods=['POST'])
def create_task():
    if not request.json or 'balance' not in request.json:
        abort(400)
    task = {
        'id': users[-1]['id'] + 1,
        'balance': request.json['balance'],
        'Add date': request.json.get('Add date', ""),
        'done': False
    }
    users.append(task)
    return jsonify({'task': task}), 201


if __name__ == '__main__':
    app.run(debug=True)
