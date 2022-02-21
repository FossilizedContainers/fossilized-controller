import lipd
from flask import *
from lipd import *
from json import *

# class allows the user to call pythonAdapter.server to get the data from the controller
class pythonAdapter:

    app = Flask(__name__)

    # will add more as we build
    def __init__(self):
        pass

    # function to read the lipd files and store them in variables
    @app.route('/', methods=['POST'])
    def server(self):
        metadata = json.loads(request.files['metadata.json'].read())
        parameters = self.get_parameters(metadata)
        inputs = self.get_files(metadata)

        # read the input lipd files
        input_lipds = {}
        for entry in inputs:
            file = request.files[entry]
            file.save(entry)
            input_lipds[entry] = lipd.readLipd("./" + entry)

        # here we would pass parameters & input_lipds to the climate model
        # passing the parameters and inputs into the climate model
        print(parameters)
        print(input_lipds)

        # the file(s) generated being returned from their directory - temporary test file for now
        return send_from_directory("./static/", "test.nc")

    # function to get the list of parameters from the json file
    def get_parameters(self, metadata):
        # using the json key "parameters" to return the parameters
        return metadata['parameters']

    # function to get the list of files from the json file
    def get_files(self, metadata):
        # using the json key "inputs" to return the files
        return metadata['inputs']

    # setting the host and port for the server to run on
    app.run(host='0.0.0.0', port=4000)
