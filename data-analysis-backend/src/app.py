from config.settings import root_data_dir
from utils.fileutils import get_all_data_files
from utils.dateutils import have_same_day, have_same_month
from ml.linearregression import run_lin_reg
from ml.logisticregression import NumberGuessingGame
from ml.guessnumber import NumberGuessingGameNN
from os.path import exists
from os import makedirs
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import numpy as np
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/files')
def get_files():
    """
    This route returns a list of all files the user may analyze
    """
    return jsonify([{"id": file["id"], "name": file["name"]} for file in files])


@app.route('/fields')
def get_fields():
    req = request.args
    return jsonify(files_dict[req['file_id']]['data_collection'].fields)


@app.route('/field_metadata')
def get_field_metadata():
    req = request.args
    return jsonify(files_dict[req['file_id']]['data_collection'].field_metadata)


@app.route('/data')
def get_data():
    """
    This route returns a json formatted array containing two arrays. This returned data may be plotted.
    The first array contains values to put on the x-axis, the second array contains data for the y-axis.
    """
    req = request.args
    data_collection = files_dict[req['file_id']]['data_collection']
    file_data = data_collection.data
    x_field = req['xField']
    y_field = req['yField']
    if x_field == 'null' or y_field == 'null':
        abort(400)
    if req['sortByX'] == 'true':
        file_data = sorted(file_data.copy(), key=lambda a: a[x_field])
    result = []
    if req['frequency'] == 'NONE' or data_collection.field_metadata[x_field] != 'date':
        result = [
            [x[x_field] for x in file_data],
            [x[y_field] for x in file_data]
        ]
    elif req['frequency'] == 'DAILY':
        result = [[file_data[0][x_field]], [file_data[0][y_field]]]
        for i in range(1, len(file_data)):
            if have_same_day(file_data[i - 1][x_field], file_data[i][x_field]):
                result[1][-1] += file_data[i][y_field]
            else:
                result[0].append(file_data[i][x_field])
                result[1].append(file_data[i][y_field])
        for i in range(0, len(result[1])):
            result[1][i] = -1 * result[1][i]
    elif req['frequency'] == 'MONTHLY':
        result = [[file_data[0][x_field].replace(day=1)], [file_data[0][y_field]]]
        for i in range(1, len(file_data)):
            if have_same_month(file_data[i-1][x_field], file_data[i][x_field]):
                result[1][-1] += file_data[i][y_field]
            else:
                result[0].append(file_data[i][x_field].replace(day=1))
                result[1].append(file_data[i][y_field])
        for i in range(0, len(result[1])):
            result[1][i] = -1 * result[1][i]
    else:
        abort(400)
    if data_collection.field_metadata[x_field] == 'date':
        for i in range(len(result[0])):
            result[0][i] = result[0][i].isoformat()
    if data_collection.field_metadata[y_field] == 'date':
        for i in range(len(result[1])):
            result[1][i] = result[1][i].isoformat()
    theta = None
    if data_collection.field_metadata[x_field] == 'number':
        theta = list(run_lin_reg(np.array([0, 0]), np.array([[x] for x in result[0]]), np.array(result[1])))
    returnable_result = {
        "x_values": result[0],
        "y_values": result[1],
        "theta": theta if theta is not None else [],
        "lin_reg_y_values": [theta[0] + x*theta[1] for x in result[0]] if theta is not None else [],
    }
    return jsonify(returnable_result)


@app.route('/numbergame', methods=['POST'])
def get_numbergame_guess():
    x_input = np.array(request.json['transformed_array'])
    return jsonify({'guess': int(num_game_nn.guess_number(x_input)[0])})


@app.route('/numbergame/train', methods=['POST'])
def train_numbergame():
    x_input = np.array(request.json['transformed_array'])
    y_input = np.array([request.json['y_value']])
    num_game_nn.train_with_new_data(x_input, y_input)
    return {
        'status': 'success'
    }


if __name__ == '__main__':
    # Load data files, create data directory if it doesn't exist
    if not exists(root_data_dir):
        makedirs(root_data_dir)
    [files, files_dict] = get_all_data_files(root_data_dir)
    # num_game = NumberGuessingGame()
    num_game_nn = NumberGuessingGameNN()
    app.run(port=5000)
