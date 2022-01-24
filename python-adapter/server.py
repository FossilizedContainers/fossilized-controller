import flask
import lipd
import json
from flask import Flask
from flask import send_from_directory
from flask import request
from lipd import readLipd

app = Flask(__name__)


@app.route('/', methods=['POST'])
def receiveLiPD():
    metadata = json.loads(request.files['metadata.json'].read())
    parameters = metadata['parameters']
    inputs = metadata['inputs']

    # read the input lipd files
    input_lipds = {}
    for input in inputs:
        file = request.files[input]
        file.save(input)
        input_lipds[input] = lipd.readLipd("./" + input)

    # here we would pass parameters & input_lipds to the climate model
    print(parameters)
    print(input_lipds)

    # fake NetCDF file that would really come from the climate model
    return send_from_directory("./static/", "test.nc")


# setting the host and port for the server to run on
app.run(host='0.0.0.0', port=4000)
